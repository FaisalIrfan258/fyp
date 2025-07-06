from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
import uuid
import os
import logging
import time
from typing import List, Optional
import shutil
from pathlib import Path

from app.models.database import Prediction, Feedback, get_db
from app.services.model_service import get_model_service
from app.utils.config import settings

logger = logging.getLogger(__name__)

# Create API router
api_router = APIRouter()

# Health check endpoint
@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    model_service = get_model_service()
    return {
        "status": "ok",
        "model_loaded": model_service.is_model_loaded(),
        "timestamp": time.time()
    }

# Prediction endpoint
@api_router.post("/predict")
async def predict_image(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Process an uploaded image and return tumor prediction"""
    # Validate file extension
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File extension not allowed. Allowed extensions: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    try:
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get model service
        model_service = get_model_service()
        
        # Perform prediction
        result = model_service.predict(file_path)
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Prediction failed: {result.get('error', 'Unknown error')}"
            )
        
        # Generate prediction ID
        prediction_id = str(uuid.uuid4())
        
        # Create session ID if not provided
        user_session = str(uuid.uuid4())
        
        # Save prediction to database
        db_prediction = Prediction(
            id=None,  # Auto-incremented
            filename=unique_filename,
            prediction=result["prediction"]["class"],
            confidence=result["prediction"]["confidence"],
            probability=result["prediction"]["probability"],
            processing_time=result["prediction"]["processing_time"],
            user_session=user_session
        )
        
        db.add(db_prediction)
        await db.commit()
        await db.refresh(db_prediction)
        
        # Return result
        return {
            "success": True,
            "prediction": result["prediction"],
            "image_info": result["image_info"],
            "timestamp": time.time(),
            "prediction_id": db_prediction.id,
            "image_url": f"/uploads/{unique_filename}"
        }
    
    except Exception as e:
        logger.error(f"Error processing prediction: {str(e)}")
        # Clean up file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing prediction: {str(e)}"
        )

# Get predictions history
@api_router.get("/predictions")
async def get_predictions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    user_session: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get prediction history with pagination"""
    try:
        # Build query
        query = select(Prediction).order_by(desc(Prediction.timestamp))
        
        # Filter by user session if provided
        if user_session:
            query = query.filter(Prediction.user_session == user_session)
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        # Execute query
        result = await db.execute(query)
        predictions = result.scalars().all()
        
        # Count total
        count_query = select(Prediction)
        if user_session:
            count_query = count_query.filter(Prediction.user_session == user_session)
        count_result = await db.execute(count_query)
        total_count = len(count_result.scalars().all())
        
        # Format results
        formatted_predictions = []
        for pred in predictions:
            formatted_predictions.append({
                "id": pred.id,
                "filename": pred.filename,
                "prediction": pred.prediction,
                "confidence": pred.confidence,
                "probability": pred.probability,
                "processing_time": pred.processing_time,
                "timestamp": pred.timestamp.isoformat(),
                "image_url": f"/uploads/{pred.filename}"
            })
        
        return {
            "predictions": formatted_predictions,
            "total": total_count,
            "skip": skip,
            "limit": limit
        }
    
    except Exception as e:
        logger.error(f"Error retrieving predictions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving predictions: {str(e)}"
        )

# Submit feedback
@api_router.post("/feedback")
async def submit_feedback(
    prediction_id: int = Form(...),
    is_correct: bool = Form(...),
    comment: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """Submit feedback for a prediction"""
    try:
        # Check if prediction exists
        result = await db.execute(
            select(Prediction).filter(Prediction.id == prediction_id)
        )
        prediction = result.scalars().first()
        
        if not prediction:
            raise HTTPException(
                status_code=404,
                detail=f"Prediction with ID {prediction_id} not found"
            )
        
        # Create feedback
        feedback = Feedback(
            prediction_id=prediction_id,
            is_correct=1 if is_correct else 0,
            comment=comment
        )
        
        db.add(feedback)
        await db.commit()
        
        return {
            "success": True,
            "message": "Feedback submitted successfully",
            "feedback_id": feedback.id
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error submitting feedback: {str(e)}"
        ) 