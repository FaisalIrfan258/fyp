import os
import time
import logging
import torch
import torch.nn as nn
from torch.nn import functional as F
from torchvision import models, transforms
from torchvision.models import ResNet18_Weights
from PIL import Image
import numpy as np
import cv2
from pathlib import Path

from app.utils.config import settings

logger = logging.getLogger(__name__)

class BrainTumorClassifier(nn.Module):
    def __init__(self, pretrained=True):
        super(BrainTumorClassifier, self).__init__()
        self.backbone = models.resnet18(weights=ResNet18_Weights.DEFAULT if pretrained else None)
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 1)
        )
    
    def forward(self, x):
        return self.backbone(x)


class ModelService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
            cls._instance._model = None
            cls._instance._device = torch.device("cpu")
            cls._instance._transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            cls._instance._load_model()
        return cls._instance
    
    def _load_model(self):
        """Load the PyTorch model from the specified path"""
        try:
            logger.info(f"Loading model from {settings.MODEL_PATH}")
            
            # Check if model file exists
            if not os.path.exists(settings.MODEL_PATH):
                logger.warning(f"Model file not found at {settings.MODEL_PATH}. Creating a new model.")
                self._model = BrainTumorClassifier(pretrained=True)
                self._model.to(self._device)
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(settings.MODEL_PATH), exist_ok=True)
                
                # Save the model
                torch.save(self._model.state_dict(), settings.MODEL_PATH)
                logger.info(f"Created and saved new model to {settings.MODEL_PATH}")
            else:
                # Load the model
                self._model = BrainTumorClassifier(pretrained=False)
                
                # Load checkpoint
                checkpoint = torch.load(settings.MODEL_PATH, map_location=self._device)
                
                # Handle different model file formats
                if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
                    # This is a training checkpoint with model_state_dict
                    logger.info("Loading model from training checkpoint format")
                    self._model.load_state_dict(checkpoint["model_state_dict"])
                elif isinstance(checkpoint, dict) and all(k.startswith("backbone.") for k in checkpoint.keys() if not k.startswith("_")):
                    # This is a direct state dict for our model
                    logger.info("Loading model from direct state dict format")
                    self._model.load_state_dict(checkpoint)
                else:
                    # Try to create a new model
                    logger.warning("Could not load model from file. Creating a new model.")
                    self._model = BrainTumorClassifier(pretrained=True)
                    
                    # Save the new model
                    torch.save(self._model.state_dict(), settings.MODEL_PATH + ".new")
                    logger.info(f"Created and saved new model to {settings.MODEL_PATH}.new")
                
                self._model.to(self._device)
                logger.info("Model loaded successfully")
            
            # Set model to evaluation mode
            self._model.eval()
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            # Create a new model as fallback
            logger.info("Creating a new model as fallback")
            self._model = BrainTumorClassifier(pretrained=True)
            self._model.to(self._device)
            self._model.eval()
    
    def is_model_loaded(self):
        """Check if the model is loaded"""
        return self._model is not None
    
    def preprocess_image(self, image_path):
        """Preprocess the image for model input"""
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            # Get original image size
            original_size = image.size
            
            # Apply transformations
            tensor = self._transform(image)
            
            return {
                "tensor": tensor.unsqueeze(0),  # Add batch dimension
                "original_size": original_size,
                "processed_size": (224, 224)
            }
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise
    
    def predict(self, image_path):
        """Perform prediction on an image"""
        if not self.is_model_loaded():
            raise RuntimeError("Model is not loaded")
        
        try:
            start_time = time.time()
            
            # Preprocess image
            preprocessed = self.preprocess_image(image_path)
            tensor = preprocessed["tensor"]
            
            # Move tensor to device
            tensor = tensor.to(self._device)
            
            # Perform inference
            with torch.no_grad():
                output = self._model(tensor)
                probability = torch.sigmoid(output).item()
            
            # Determine class and confidence
            prediction = "tumor" if probability >= 0.5 else "no_tumor"
            confidence = probability if prediction == "tumor" else 1 - probability
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            return {
                "success": True,
                "prediction": {
                    "class": prediction,
                    "confidence": float(confidence),
                    "probability": float(probability),
                    "processing_time": processing_time
                },
                "image_info": {
                    "original_size": preprocessed["original_size"],
                    "processed_size": preprocessed["processed_size"],
                    "file_size": os.path.getsize(image_path)
                }
            }
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }


# Singleton instance getter
def get_model_service():
    return ModelService() 