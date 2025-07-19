from sqlalchemy import Column, Integer, String, Text, Boolean
from .database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    scraped_text = Column(Text, nullable=False)
    model_prediction = Column(String, nullable=False)
    user_feedback_is_correct = Column(Boolean, nullable=False)
