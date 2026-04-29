from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.generation import GenerationHistory

router = APIRouter()

@router.get("/api/v1/history")
def get_history(db: Session = Depends(get_db), limit: int = 20):
    records = db.query(GenerationHistory).order_by(GenerationHistory.created_at.desc()).limit(limit).all()
    return records