from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from app.services import scraper, analysis
from app import models
from app.database import get_db

router = APIRouter()

class FeedbackCreate(BaseModel):
    scraped_text: str
    model_prediction: str
    is_correct: bool

@router.post("/analyze")
async def analyze_entity(entity_name: str):
    """
    This endpoint now returns a list of articles AND an overall risk assessment.
    """
    scraped_articles = await scraper.scrape_web(entity_name)
    analyzed_articles = analysis.analyze_articles(scraped_articles)
    
    # --- NEW: Calculate Overall Risk ---
    overall_risk = "LOW" # Default to LOW
    risk_levels = [article['risk_level'] for article in analyzed_articles]
    
    if "HIGH" in risk_levels:
        overall_risk = "HIGH"
    elif "MEDIUM" in risk_levels:
        overall_risk = "MEDIUM"
    # ------------------------------------

    return {"articles": analyzed_articles, "overall_risk": overall_risk}

@router.post("/feedback")
def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = models.Feedback(
        scraped_text=feedback.scraped_text,
        model_prediction=feedback.model_prediction,
        user_feedback_is_correct=feedback.is_correct
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return {"status": "success", "feedback_id": db_feedback.id}

@router.get("/dashboard-data")
def get_dashboard_data(db: Session = Depends(get_db)):
    query_result = db.query(
        models.Feedback.model_prediction, 
        func.count(models.Feedback.model_prediction).label('count')
    ).group_by(models.Feedback.model_prediction).all()
    pie_chart_data = [{"name": label, "value": count} for label, count in query_result]
    return {"pieChart": pie_chart_data}