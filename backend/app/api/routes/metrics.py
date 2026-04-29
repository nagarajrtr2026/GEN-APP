from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.metric import MetricsSummary

router = APIRouter()

@router.get("/api/v1/metrics")
def get_metrics(db: Session = Depends(get_db)):
    summary = db.query(MetricsSummary).first()
    if not summary:
        return {
            "total_requests": 0,
            "success_requests": 0,
            "failed_requests": 0,
            "avg_latency": 0.0
        }
    return summary