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