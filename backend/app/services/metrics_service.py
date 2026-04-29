from sqlalchemy.orm import Session
from app.models.metric import MetricsSummary
from app.models.generation import GenerationHistory

class MetricsService:
    @staticmethod
    def record_generation(db: Session, prompt: str, provider: str, success: bool, latency: float, output: str):
        # Insert History
        history = GenerationHistory(
            prompt=prompt,
            provider=provider,
            success=success,
            latency_ms=latency,
            output_json=output
        )
        db.add(history)

        # Update Summary Document
        summary = db.query(MetricsSummary).first()
        if not summary:
            summary = MetricsSummary(
                total_requests=0,
                success_requests=0,
                failed_requests=0,
                avg_latency=0.0
            )
            db.add(summary)

        # Recalculate average
        current_total = summary.total_requests
        current_avg = summary.avg_latency
        
        new_total = current_total + 1
        new_avg = ((current_avg * current_total) + latency) / new_total
        
        summary.total_requests = new_total
        summary.avg_latency = new_avg
        
        if success:
            summary.success_requests += 1
        else:
            summary.failed_requests += 1

        db.commit()