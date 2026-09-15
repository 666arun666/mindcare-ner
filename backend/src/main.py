from backend.src.core.config import settings
from backend.src.core.database import Base, engine
from backend.src.routers import auth, patients, sync
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize database schema
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for MINDCARE NER cognitive gaming and memory assistance platform.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(sync.router, prefix=settings.API_V1_STR)
app.include_router(patients.router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["health"])
def health_check():
    return {
        "status": "healthy",
        "service": "MINDCARE NER Backend",
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT,
    }
