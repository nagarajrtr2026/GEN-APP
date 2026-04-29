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