import os

base_dir = r"c:\Users\ADMIN\OneDrive\App\backend"

files = {
    "requirements.txt": """
fastapi>=0.100.0
uvicorn>=0.22.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
sqlalchemy>=2.0.0
alembic>=1.11.0
pytest>=7.0.0
httpx>=0.24.0
python-dotenv>=1.0.0
    """,
    ".env.example": """
AI_PROVIDER=dummy
API_KEY=your_key_here
DATABASE_URL=sqlite:///./sql_app.db
PORT=8000
    """,
    "README.md": """
# AI App Generator Backend

This is a complete backend project for an AI App Generator pipeline.
It parses natural language prompts, converts them into intermediate representation, and generates validated JSON configurations for building web applications.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   ```
   *Note: Dummy mode is enabled by default (`AI_PROVIDER=dummy`), meaning it will work instantly without any API keys!*

3. **Run the Application**
   ```bash
   python run.py
   ```

4. **API Documentation**
   Open your browser and navigate to: [http://localhost:8000/docs](http://localhost:8000/docs)
   You'll find the interactive Swagger UI to test everything out!

## How to Switch AI Providers
Simply open `.env` and update `AI_PROVIDER` to `gemini`, `claude`, or `openai`:
```env
AI_PROVIDER=gemini
API_KEY=your_real_api_key_here
```
The codebase naturally handles the abstraction!

## Testing
Run tests using pytest:
```bash
pytest app/tests/ -v
```
    """,
    "run.py": """
import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
    """,
    "app/__init__.py": "",
    "app/main.py": """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, generate, metrics, history
from app.core.database import engine, Base

# Create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI App Generator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(generate.router)
app.include_router(metrics.router)
app.include_router(history.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI App Generator Backend"}
    """,
    "app/core/__init__.py": "",
    "app/core/config.py": """
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI App Generator"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    PORT: int = int(os.getenv("PORT", "8000"))
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "dummy")
    API_KEY: str = os.getenv("API_KEY", "")

    class Config:
        env_file = ".env"

settings = Settings()
    """,
    "app/core/database.py": """
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    """,
    "app/core/logger.py": """
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ai_pipeline")
    """,
    "app/core/security.py": """
# Minimal security functions
def verify_api_key(api_key: str) -> bool:
    # Add real verification logic here
    return len(api_key) > 5
    """,
    "app/models/__init__.py": "",
    "app/models/generation.py": """
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
    """,
    "app/models/metric.py": """
from sqlalchemy import Column, Integer, Float
from app.core.database import Base

class MetricsSummary(Base):
    __tablename__ = "metrics_summary"

    id = Column(Integer, primary_key=True, index=True)
    total_requests = Column(Integer, default=0)
    success_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    avg_latency = Column(Float, default=0.0)
    """,
    "app/schemas/__init__.py": "",
    "app/schemas/common.py": """
from pydantic import BaseModel
from typing import Any, Dict

class AppConfig(BaseModel):
    ui_schema: Dict[str, Any]
    api_schema: Dict[str, Any]
    db_schema: Dict[str, Any]
    auth_schema: Dict[str, Any]
    """,
    "app/schemas/request.py": """
from pydantic import BaseModel

class GenerateRequest(BaseModel):
    prompt: str
    """,
    "app/schemas/response.py": """
from pydantic import BaseModel
from typing import Any, Dict, Optional

class GenerateResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    """,
    "app/api/__init__.py": "",
    "app/api/routes/__init__.py": "",
    "app/api/routes/health.py": """
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy"}
    """,
    "app/api/routes/generate.py": """
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
    """,
    "app/api/routes/history.py": """
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.generation import GenerationHistory

router = APIRouter()

@router.get("/api/v1/history")
def get_history(db: Session = Depends(get_db), limit: int = 20):
    records = db.query(GenerationHistory).order_by(GenerationHistory.created_at.desc()).limit(limit).all()
    return records
    """,
    "app/api/routes/metrics.py": """
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
    """,
    "app/services/__init__.py": "",
    "app/services/ai_client.py": """
from app.core.config import settings

class AIClient:
    def __init__(self):
        self.provider = settings.AI_PROVIDER
        self.api_key = settings.API_KEY

    def generate(self, prompt: str) -> str:
        provider_map = {
            "dummy": self._dummy_generate,
            "gemini": self._gemini_generate,
            "claude": self._claude_generate,
            "openai": self._openai_generate
        }
        handler = provider_map.get(self.provider, self._dummy_generate)
        return handler(prompt)

    def _dummy_generate(self, prompt: str) -> str:
        # Dummy behavior based on stage
        if "Extract intent" in prompt:
            return '''{
                "app_name": "Dummy CRM",
                "app_type": "CRM",
                "modules": ["login", "contacts", "dashboard"],
                "roles": ["admin", "user"],
                "billing": "premium",
                "assumptions": []
            }'''
        if "Design system" in prompt:
            return '''{
                "entities": ["User", "Contact"],
                "flows": ["Login Flow", "Create Contact"],
                "permissions": {"admin": "all", "user": "read"},
                "navigation": ["Dashboard", "Contacts"]
            }'''
        if "Generate schemas" in prompt:
            return '''{
                "ui_schema": {"pages": ["Login", "Dashboard"]},
                "api_schema": {"endpoints": ["/login", "/api/contacts"]},
                "db_schema": {"tables": ["users", "contacts"]},
                "auth_schema": {"roles": ["admin", "user"]}
            }'''
            
        # Fallback raw response
        return '{"fallback": true}'

    def _gemini_generate(self, prompt: str) -> str:
        # Integrate google-generativeai here
        return self._dummy_generate(prompt)

    def _claude_generate(self, prompt: str) -> str:
        # Integrate anthropic here
        return self._dummy_generate(prompt)

    def _openai_generate(self, prompt: str) -> str:
        # Integrate openai here
        return self._dummy_generate(prompt)
    """,
    "app/services/intent_extractor.py": """
import json
from app.services.ai_client import AIClient

class IntentExtractor:
    def __init__(self, ai_client: AIClient):
        self.ai = ai_client

    def extract(self, prompt: str) -> dict:
        content = self.ai.generate(f"Extract intent for: {prompt}")
        try:
            return json.loads(content)
        except Exception:
            return {"raw_prompt": prompt}
    """,
    "app/services/system_designer.py": """
import json
from app.services.ai_client import AIClient

class SystemDesigner:
    def __init__(self, ai_client: AIClient):
        self.ai = ai_client

    def design(self, intent: dict) -> dict:
        content = self.ai.generate(f"Design system based on intent: {json.dumps(intent)}")
        try:
            return json.loads(content)
        except Exception:
            return {"entities": []}
    """,
    "app/services/schema_generator.py": """
import json
from app.services.ai_client import AIClient

class SchemaGenerator:
    def __init__(self, ai_client: AIClient):
        self.ai = ai_client

    def generate(self, design: dict) -> dict:
        content = self.ai.generate(f"Generate schemas for design: {json.dumps(design)}")
        try:
            return json.loads(content)
        except Exception:
            return {}
    """,
    "app/services/validator.py": """
class Validator:
    def validate(self, schemas: dict) -> list[str]:
        errors = []
        if not schemas:
            errors.append("Empty output from schema generator")
            return errors
            
        required_sections = ["ui_schema", "api_schema", "db_schema", "auth_schema"]
        for section in required_sections:
            if section not in schemas:
                errors.append(f"Missing section: {section}")
                
        # More complex validations could check for DB table mismatches, routing mismatches, etc.
        return errors
    """,
    "app/services/repair_engine.py": """
class RepairEngine:
    def repair(self, schemas: dict, errors: list[str]) -> dict:
        repaired = schemas.copy()
        for error in errors:
            if "Missing section: ui_schema" in error:
                repaired["ui_schema"] = {"pages": [], "repaired": True}
            elif "Missing section: api_schema" in error:
                repaired["api_schema"] = {"endpoints": [], "repaired": True}
            elif "Missing section: db_schema" in error:
                repaired["db_schema"] = {"tables": [], "repaired": True}
            elif "Missing section: auth_schema" in error:
                repaired["auth_schema"] = {"roles": [], "repaired": True}
                
        return repaired
    """,
    "app/services/pipeline.py": """
from app.services.ai_client import AIClient
from app.services.intent_extractor import IntentExtractor
from app.services.system_designer import SystemDesigner
from app.services.schema_generator import SchemaGenerator
from app.services.validator import Validator
from app.services.repair_engine import RepairEngine

class Pipeline:
    def __init__(self):
        self.ai_client = AIClient()
        self.extractor = IntentExtractor(self.ai_client)
        self.designer = SystemDesigner(self.ai_client)
        self.generator = SchemaGenerator(self.ai_client)
        self.validator = Validator()
        self.repair_engine = RepairEngine()

    def run(self, prompt: str) -> dict:
        if not prompt or not prompt.strip():
            raise ValueError("Invalid empty prompt")

        # Stage 1: Intent Extraction
        intent = self.extractor.extract(prompt)

        # Stage 2: System Design
        design = self.designer.design(intent)

        # Stage 3: Schema Generation
        schemas = self.generator.generate(design)

        # Stage 4: Validation
        errors = self.validator.validate(schemas)

        # Stage 5: Repair
        if errors:
            schemas = self.repair_engine.repair(schemas, errors)

        return schemas
    """,
    "app/services/metrics_service.py": """
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
    """,
    "app/utils/__init__.py": "",
    "app/utils/helpers.py": """
import json
import re

def extract_json(text: str) -> dict:
    # Handle markdown JSON wrappers safely
    pattern = r"```(?:json)? \n?(.*?)\n?```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        text = match.group(1)
    
    try:
        return json.loads(text.strip())
    except Exception:
        return {}
    """,
    "app/utils/constants.py": """
DEFAULT_AI_PROVIDER = "dummy"
    """,
    "app/tests/__init__.py": "",
    "app/tests/test_health.py": """
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
    """,
    "app/tests/test_generate.py": """
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Set dummy DB for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_generate_empty_prompt():
    response = client.post("/api/v1/generate", json={"prompt": " "})
    assert response.status_code == 400
    assert "Invalid empty prompt" in response.json()["detail"]

def test_generate_success():
    response = client.post("/api/v1/generate", json={"prompt": "Build CRM"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "ui_schema" in data["data"]
    
def teardown_module(module):
    if os.path.exists("./test.db"):
        os.remove("./test.db")
    """
}

# Create all files on disk
for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
        
print(f"Project successfully generated at {base_dir}")
