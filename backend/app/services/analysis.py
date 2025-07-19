from transformers import pipeline
from typing import List, Dict

# IMPORTANT: Make sure this points to your fine-tuned model on the Hub!
HF_MODEL_REPO_NAME = "Bats1107/scouse-ai-finbert-classifier"

# Load your fine-tuned model from the Hub
risk_classifier = pipeline(
    "text-classification", 
    model=HF_MODEL_REPO_NAME
)

def analyze_articles(articles: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Analyzes a list of articles, assigning a risk level to each one.
    """
    if not articles:
        return []

    # Extract just the titles for batch processing
    titles_to_analyze = [article['title'] for article in articles]
    
    # Get risk predictions for all titles in a single batch (much faster)
    predictions = risk_classifier(titles_to_analyze)

    # Add the prediction back to each original article object
    for i, article in enumerate(articles):
        article['risk_level'] = predictions[i]['label']
        article['risk_score'] = predictions[i]['score']

    return articles