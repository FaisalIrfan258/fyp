from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging
from pathlib import Path

from app.api.routes import api_router
from app.utils.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Brain Tumor Detection API",
    description="API for brain tumor detection using deep learning",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Mount uploads directory for serving uploaded images
uploads_path = Path(settings.UPLOAD_DIR)
if not uploads_path.exists():
    uploads_path.mkdir(parents=True, exist_ok=True)
    
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

@app.get("/")
async def root():
    return {
        "message": "Brain Tumor Detection API",
        "docs_url": "/docs",
        "health_check": "/api/health"
    }

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Brain Tumor Detection API")
    # Ensure required directories exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    from app.models.database import init_db
    await init_db()
    
    from app.services.model_service import get_model_service
    # Initialize model service (this will load the model)
    model_service = get_model_service()
    logger.info(f"Model loaded successfully: {model_service.is_model_loaded()}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Brain Tumor Detection API") 