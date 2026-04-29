from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.request import GenerateRequest
from app.schemas.response import GenerateResponse
from app.core.database import get_db
from app.services.pipeline import Pipeline
from app.services.metrics_service import MetricsService
from app.core.config import settings
import time
import json

router = APIRouter()

@router.post("/api/v1/generate", response_model=GenerateResponse)
def generate_app(req: GenerateRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    
    # Initialize pipeline
    pipeline = Pipeline()
    
    try:
        data = pipeline.run(req.prompt)
        latency_ms = (time.time() - start_time) * 1000
        
        # Save metrics
        MetricsService.record_generation(
            db=db,
            prompt=req.prompt,
            provider=settings.AI_PROVIDER,
            success=True,
            latency=latency_ms,
            output=json.dumps(data)
        )
        return GenerateResponse(success=True, data=data)
        
    except ValueError as e:
        latency_ms = (time.time() - start_time) * 1000
        MetricsService.record_generation(
            db=db, prompt=req.prompt, provider=settings.AI_PROVIDER, success=False, latency=latency_ms, output=str(e)
        )
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        MetricsService.record_generation(
            db=db, prompt=req.prompt, provider=settings.AI_PROVIDER, success=False, latency=latency_ms, output=str(e)
        )
        raise HTTPException(status_code=500, detail="Internal server error")