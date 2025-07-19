import evaluate
import numpy as np
from datasets import load_dataset, Features, ClassLabel, Value
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding, 
)
from huggingface_hub import HfFolder, whoami

# --- Configuration ---
MODEL_NAME = "ProsusAI/finbert"
DATASET_FILE = "ml/risk-dataset-augmented.csv" 
# IMPORTANT: Change this to your Hugging Face username!
HF_MODEL_REPO_NAME = "Bats1107/scouse-ai-finbert-classifier" 

# --- 1. Load and Prepare the Dataset ---
print(f"Loading dataset from {DATASET_FILE}...")

class_labels = ClassLabel(names=["LOW", "MEDIUM", "HIGH"])
features = Features({
    "text": Value("string"),
    "label": class_labels,
})

dataset = load_dataset("csv", data_files=DATASET_FILE, features=features)

labels = dataset["train"].features["label"].names
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for i, label in enumerate(labels)}

# --- 2. Preprocess and Tokenize ---
print("Tokenizing dataset...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)

tokenized_dataset = dataset.map(preprocess_function, batched=True)
tokenized_dataset = tokenized_dataset.rename_column("label", "labels")
tokenized_dataset = tokenized_dataset.remove_columns(["text"])

train_test_split = tokenized_dataset["train"].train_test_split(test_size=0.1)
train_dataset = train_test_split["train"]
eval_dataset = train_test_split["test"]

# --- 3. Define the Model and Metrics ---
print("Loading model...")
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME, num_labels=len(labels), id2label=id2label, label2id=label2id
)

accuracy_metric = evaluate.load("accuracy")
f1_metric = evaluate.load("f1")

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    acc = accuracy_metric.compute(predictions=predictions, references=labels)
    f1 = f1_metric.compute(predictions=predictions, references=labels, average="weighted")
    return {"accuracy": acc["accuracy"], "f1": f1["f1"]}

# --- 4. Set Up The Trainer ---
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# --- THIS IS THE FINAL FIX ---
# We are now explicitly setting evaluation_strategy to match save_strategy.
training_args = TrainingArguments(
    output_dir="ml/training_output",
    num_train_epochs=3, 
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    logging_strategy="epoch",
    save_strategy="epoch",
    evaluation_strategy="epoch", # This line fixes the error
    load_best_model_at_end=True,
    push_to_hub=True,
    hub_model_id=HF_MODEL_REPO_NAME,
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# --- 5. Train and Push to Hub ---
print("Starting training...")
trainer.train()

print("Training complete. Pushing model to Hugging Face Hub...")
trainer.push_to_hub()
print("Model successfully pushed to the Hub!")