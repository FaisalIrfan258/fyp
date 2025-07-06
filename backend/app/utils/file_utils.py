import os
import time
import logging
from pathlib import Path
import shutil
from app.utils.config import settings

logger = logging.getLogger(__name__)

def is_valid_file_extension(filename: str) -> bool:
    """Check if the file has an allowed extension"""
    return filename.split(".")[-1].lower() in settings.ALLOWED_EXTENSIONS

def is_valid_file_size(file_size: int) -> bool:
    """Check if the file size is within allowed limits"""
    return file_size <= settings.MAX_FILE_SIZE

def clean_old_files(directory: str = None, max_age: int = None):
    """Delete files older than max_age seconds"""
    if directory is None:
        directory = settings.UPLOAD_DIR
    
    if max_age is None:
        max_age = settings.MAX_FILE_AGE
    
    try:
        now = time.time()
        count = 0
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Check file age
            file_age = now - os.path.getmtime(file_path)
            
            if file_age > max_age:
                os.remove(file_path)
                count += 1
        
        logger.info(f"Cleaned {count} old files from {directory}")
        
    except Exception as e:
        logger.error(f"Error cleaning old files: {str(e)}")

def ensure_directory_exists(directory: str):
    """Ensure the specified directory exists"""
    Path(directory).mkdir(parents=True, exist_ok=True) 