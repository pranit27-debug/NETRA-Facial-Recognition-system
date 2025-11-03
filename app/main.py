"""
NETRA FastAPI Application - Main Entry Point
"""

import os
import io
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import torch
import numpy as np
from datetime import datetime

from app.model import SiameseNetwork, cosine_similarity, euclidean_distance
from app.preprocess import (
    FaceDetector, ImagePreprocessor, 
    load_image_from_bytes
)
from app.utils import load_config, get_device

# Initialize FastAPI app
app = FastAPI(
    title="NETRA Facial Recognition API",
    description="Enterprise-grade facial recognition using Siamese Neural Networks",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Global variables
model: Optional[SiameseNetwork] = None
face_detector: Optional[FaceDetector] = None
preprocessor: Optional[ImagePreprocessor] = None
device: Optional[torch.device] = None
config: dict = {}


@app.on_event("startup")
async def startup_event():
    """Initialize model and services on startup"""
    global model, face_detector, preprocessor, device, config
    
    print("🚀 Starting NETRA Facial Recognition System...")
    
    # Load configuration
    config = load_config()
    
    # Set device
    device = get_device(config.get('model', {}).get('device', 'auto'))
    print(f"📱 Using device: {device}")
    
    # Initialize face detector
    face_detector = FaceDetector()
    print("✅ Face detector initialized")
    
    # Initialize preprocessor
    image_size = config.get('data', {}).get('image_size', 160)
    preprocessor = ImagePreprocessor(image_size=image_size)
    print("✅ Image preprocessor initialized")
    
    # Load model
    model_path = config.get('model', {}).get('path', 'models/siamese.pth')
    embedding_dim = config.get('model', {}).get('embedding_dim', 128)
    backbone = config.get('model', {}).get('backbone', 'resnet50')
    
    if os.path.exists(model_path):
        model = SiameseNetwork(embedding_dim=embedding_dim, backbone=backbone)
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.to(device)
        model.eval()
        print(f"✅ Model loaded from {model_path}")
    else:
        print(f"⚠️  Model file not found at {model_path}. Starting without pre-trained model.")
        model = SiameseNetwork(embedding_dim=embedding_dim, backbone=backbone)
        model.to(device)
        model.eval()
    
    print("✨ NETRA is ready!")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "NETRA Facial Recognition System",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "device": str(device),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/ready")
async def readiness_check():
    """Readiness check for Kubernetes"""
    if model is None or face_detector is None:
        raise HTTPException(status_code=503, detail="Service not ready")
    
    return {"status": "ready"}


@app.post("/api/v1/detect")
async def detect_faces(image: UploadFile = File(...)):
    """
    Detect faces in an image
    
    Args:
        image: Image file
        
    Returns:
        JSON with detected faces
    """
    try:
        # Read image
        image_bytes = await image.read()
        img_array = load_image_from_bytes(image_bytes)
        
        # Detect faces
        faces = face_detector.detect_faces(img_array)
        
        # Format response
        formatted_faces = []
        for idx, face in enumerate(faces):
            formatted_faces.append({
                "id": idx,
                "bbox": face['bbox'],
                "confidence": float(face['confidence']),
                "area": (face['bbox'][2] - face['bbox'][0]) * (face['bbox'][3] - face['bbox'][1])
            })
        
        return {
            "status": "success",
            "face_count": len(formatted_faces),
            "faces": formatted_faces
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting faces: {str(e)}")


@app.post("/api/v1/verify")
async def verify_faces(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...),
    threshold: float = Form(0.7)
):
    """
    Verify if two face images belong to the same person
    
    Args:
        image1: First face image
        image2: Second face image
        threshold: Similarity threshold (0-1)
        
    Returns:
        JSON with verification result
    """
    try:
        # Read images
        img1_bytes = await image1.read()
        img2_bytes = await image2.read()
        
        img1_array = load_image_from_bytes(img1_bytes)
        img2_array = load_image_from_bytes(img2_bytes)
        
        # Detect faces
        faces1 = face_detector.detect_faces(img1_array)
        faces2 = face_detector.detect_faces(img2_array)
        
        if len(faces1) == 0:
            raise HTTPException(status_code=400, detail="No face detected in first image")
        if len(faces2) == 0:
            raise HTTPException(status_code=400, detail="No face detected in second image")
        
        # Extract faces
        face1_bbox = faces1[0]['bbox']
        face2_bbox = faces2[0]['bbox']
        
        x1, y1, x2, y2 = face1_bbox
        face1_crop = img1_array[y1:y2, x1:x2]
        
        x1, y1, x2, y2 = face2_bbox
        face2_crop = img2_array[y1:y2, x1:x2]
        
        # Preprocess
        tensor1 = preprocessor.preprocess_image(face1_crop).unsqueeze(0).to(device)
        tensor2 = preprocessor.preprocess_image(face2_crop).unsqueeze(0).to(device)
        
        # Get embeddings
        with torch.no_grad():
            embedding1, embedding2 = model(tensor1, tensor2)
        
        # Calculate similarity
        similarity = cosine_similarity(embedding1, embedding2)
        is_match = similarity >= threshold
        
        return {
            "status": "success",
            "similarity_score": float(similarity),
            "is_match": bool(is_match),
            "threshold_used": float(threshold)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying faces: {str(e)}")


@app.post("/api/v1/similarity")
async def calculate_similarity(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...)
):
    """
    Calculate similarity score between two face images
    
    Args:
        image1: First face image
        image2: Second face image
        
    Returns:
        JSON with similarity metrics
    """
    try:
        # Read images
        img1_bytes = await image1.read()
        img2_bytes = await image2.read()
        
        img1_array = load_image_from_bytes(img1_bytes)
        img2_array = load_image_from_bytes(img2_bytes)
        
        # Detect faces
        faces1 = face_detector.detect_faces(img1_array)
        faces2 = face_detector.detect_faces(img2_array)
        
        if len(faces1) == 0 or len(faces2) == 0:
            raise HTTPException(status_code=400, detail="Face not detected in one or both images")
        
        # Extract and preprocess faces
        face1_bbox = faces1[0]['bbox']
        face2_bbox = faces2[0]['bbox']
        
        x1, y1, x2, y2 = face1_bbox
        face1_crop = img1_array[y1:y2, x1:x2]
        
        x1, y1, x2, y2 = face2_bbox
        face2_crop = img2_array[y1:y2, x1:x2]
        
        tensor1 = preprocessor.preprocess_image(face1_crop).unsqueeze(0).to(device)
        tensor2 = preprocessor.preprocess_image(face2_crop).unsqueeze(0).to(device)
        
        # Get embeddings
        with torch.no_grad():
            embedding1, embedding2 = model(tensor1, tensor2)
        
        # Calculate metrics
        cosine_sim = cosine_similarity(embedding1, embedding2)
        euclidean_dist = euclidean_distance(embedding1, embedding2)
        
        return {
            "status": "success",
            "cosine_similarity": float(cosine_sim),
            "euclidean_distance": float(euclidean_dist),
            "normalized_similarity": float((cosine_sim + 1) / 2)  # Scale to 0-1
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating similarity: {str(e)}")


def run_server():
    """Entry point for console script"""
    import uvicorn
    
    # Load config if not already loaded
    if not config or len(config) == 0:
        cfg = load_config()
    else:
        cfg = config
    
    host = cfg.get('app', {}).get('host', '0.0.0.0')
    port = cfg.get('app', {}).get('port', 8000)
    workers = cfg.get('app', {}).get('workers', 4)
    reload = cfg.get('app', {}).get('reload', False)
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        workers=1 if reload else workers,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    run_server()
