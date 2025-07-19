import pandas as pd
import evaluate
import numpy as np
from datasets import Dataset, Features, ClassLabel, Value
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
)
from sqlalchemy import create_engine
from datetime import datetime

# --- Configuration ---
# IMPORTANT: Change these to your actual details
HF_MODEL_REPO_NAME = "your-username/scouse-ai-risk-classifier"
DATABASE_URL = "postgresql://dbansal22:your_password@localhost:5432/scouseai_feedback"
ORIGINAL_DATASET_FILE = "ml/risk-dataset.csv"
MODEL_NAME = "distilbert-base-uncased"

# --- 1. Load Data ---
print("Loading data...")

# Load original dataset
original_df = pd.read_csv(ORIGINAL_DATASET_FILE)

# Load feedback data from the database
engine = create_engine(DATABASE_URL)
feedback_df = pd.read_sql("SELECT scraped_text, model_prediction, user_feedback_is_correct FROM feedback", engine)

print(f"Loaded {len(original_df)} original examples and {len(feedback_df)} feedback examples.")

# --- 2. Process Feedback Data ---
# We only want to learn from the feedback where the user corrected our model.
# If the user said our prediction was correct, we can use it, but the most valuable data
# is when they tell us we were wrong.

processed_feedback = []
for _, row in feedback_df.iterrows():
    if not row['user_feedback_is_correct']:
        # The user said the model was wrong. We need to figure out the correct label.
        # This is a simplified approach. A real system might have a UI for this.
        # For now, we'll make an assumption: if the model said HIGH, the user implies MEDIUM/LOW.
        # We will flip HIGH to MEDIUM as a conservative correction.
        correct_label = "MEDIUM" if row['model_prediction'] == 'HIGH' else 'HIGH'
    else:
        # The user confirmed our prediction was correct.
        correct_label = row['model_prediction']
    
    processed_feedback.append({'text': row['scraped_text'], 'label': correct_label})

feedback_df_processed = pd.DataFrame(processed_feedback)

# --- 3. Combine Datasets ---
combined_df = pd.concat([original_df, feedback_df_processed], ignore_index=True)
print(f"Total examples for retraining: {len(combined_df)}")

# Convert to Hugging Face Dataset object
features = Features({
    "text": Value("string"),
    "label": ClassLabel(names=["LOW", "MEDIUM", "HIGH"]),
})
dataset = Dataset.from_pandas(combined_df, features=features)

# --- 4. Prepare for Training (Tokenize, Split, etc.) ---
# (This section is the same as the original training script)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
def preprocess_function(examples):
    tokenized_inputs = tokenizer(examples["text"], truncation=True, padding=True)
    tokenized_inputs["labels"] = examples["label"]
    return tokenized_inputs

tokenized_dataset = dataset.map(preprocess_function, batched=True, remove_columns=dataset.column_names)
train_test_split = tokenized_dataset.train_test_split(test_size=0.2)
train_dataset = train_test_split["train"]
eval_dataset = train_test_split["test"]

# --- 5. Load Model and Set Up Trainer ---
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3)
accuracy_metric = evaluate.load("accuracy")
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy_metric.compute(predictions=predictions, references=labels)

# Create a new versioned model name for the Hub
new_model_version_name = f"{HF_MODEL_REPO_NAME}-v{datetime.now().strftime('%Y%m%d%H%M')}"

training_args = TrainingArguments(
    output_dir=f"ml/retraining_output/{new_model_version_name}",
    num_train_epochs=15,
    per_device_train_batch_size=4,
    eval_strategy="epoch",
    push_to_hub=True,
    hub_model_id=new_model_version_name,
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
)

# --- 6. Train and Push New Model ---
print(f"Starting retraining for new model version: {new_model_version_name}")
trainer.train()

print("Retraining complete. Pushing new model version to Hugging Face Hub...")
trainer.push_to_hub()
print(f"Successfully pushed {new_model_version_name} to the Hub!")