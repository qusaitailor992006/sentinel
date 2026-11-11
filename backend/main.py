import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.database import engine, Base, SessionLocal
from backend.app.models.sentinel_models import *
from backend.app.services.synthetic_engine import synthetic_generator
from backend.app.api.cases_router import router as cases_router
from backend.app.api.transactions_router import router as transactions_router
from backend.app.api.analytics_router import router as analytics_router
from backend.app.api.graph_router import router as graph_router

# Initialize database schema
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise Trust & Safety Intelligence Platform simulating fintech risk operations.",
    version="1.0.0"
)

# Enable CORS for local Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(cases_router)
app.include_router(transactions_router)
app.include_router(analytics_router)
app.include_router(graph_router)

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        # Automatically seed demonstration dataset if clean
        synthetic_generator.seed_initial_platform_data(db)
    finally:
        db.close()

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "platform": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=settings.PORT, reload=True)
