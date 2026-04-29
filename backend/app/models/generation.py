from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean
from app.core.database import Base
from datetime import datetime

class GenerationHistory(Base):
    __tablename__ = "generation_history"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    provider = Column(String, nullable=False)
    success = Column(Boolean, default=False)
    latency_ms = Column(Float, default=0.0)
    output_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)