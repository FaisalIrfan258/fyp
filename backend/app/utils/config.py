import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseModel):
    # API settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Brain Tumor Detection API"
    
    # CORS settings
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # Frontend development server
        "http://localhost:8000",  # Backend development server
        "*",  # Allow all origins in development
    ]
    
    # File storage settings
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", str(BASE_DIR / "uploads"))
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10MB
    ALLOWED_EXTENSIONS: set = {"png", "jpg", "jpeg"}
    
    # Model settings
    MODEL_PATH: str = os.getenv("MODEL_PATH", str(BASE_DIR / "model_files" / "brain_tumor_model.pth"))
    
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://postgres:postgres@localhost:5432/brain_tumor_detection"
    )
    
    # Security settings
    RATE_LIMIT: int = int(os.getenv("RATE_LIMIT", 100))  # Requests per minute
    
    # Cleanup settings
    CLEANUP_INTERVAL: int = int(os.getenv("CLEANUP_INTERVAL", 24 * 60 * 60))  # 24 hours
    MAX_FILE_AGE: int = int(os.getenv("MAX_FILE_AGE", 7 * 24 * 60 * 60))  # 7 days

# Create settings instance
settings = Settings()

# Create required directories
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(settings.MODEL_PATH), exist_ok=True) 