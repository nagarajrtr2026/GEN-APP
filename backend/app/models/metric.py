from sqlalchemy import Column, Integer, Float
from app.core.database import Base

class MetricsSummary(Base):
    __tablename__ = "metrics_summary"

    id = Column(Integer, primary_key=True, index=True)
    total_requests = Column(Integer, default=0)
    success_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    avg_latency = Column(Float, default=0.0)