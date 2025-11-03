"""
Image preprocessing and face detection utilities
"""

import cv2
import numpy as np
from PIL import Image
import face_recognition
from mtcnn import MTCNN
from typing import List, Tuple, Optional
import torch
import torchvision.transforms as transforms


class FaceDetector:
    """Face detection using MTCNN"""
    
    def __init__(self):
        self.detector = MTCNN()
    
    def detect_faces(self, image: np.ndarray) -> List[dict]:
        """
        Detect faces in an image
        
        Args:
            image: Input image as numpy array (RGB)
            
        Returns:
            List of detected faces with bounding boxes and confidence
        """
        results = self.detector.detect_faces(image)
        
        faces = []
        for result in results:
            x, y, width, height = result['box']
            confidence = result['confidence']
            
            faces.append({
                'bbox': [x, y, x + width, y + height],
                'confidence': confidence,
                'keypoints': result['keypoints']
            })
        
        return faces
    
    def extract_face(self, image: np.ndarray, bbox: List[int], 
                     margin: int = 20) -> Optional[np.ndarray]:
        """
        Extract face region from image
        
        Args:
            image: Input image
            bbox: Bounding box [x1, y1, x2, y2]
            margin: Margin to add around face
            
        Returns:
            Cropped face image or None
        """
        x1, y1, x2, y2 = bbox
        
        # Add margin
        x1 = max(0, x1 - margin)
        y1 = max(0, y1 - margin)
        x2 = min(image.shape[1], x2 + margin)
        y2 = min(image.shape[0], y2 + margin)
        
        face = image[y1:y2, x1:x2]
        
        if face.size == 0:
            return None
        
        return face


class ImagePreprocessor:
    """Image preprocessing pipeline"""
    
    def __init__(self, image_size: int = 160):
        self.image_size = image_size
        self.transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    def preprocess_image(self, image: np.ndarray) -> torch.Tensor:
        """
        Preprocess image for model input
        
        Args:
            image: Input image as numpy array (RGB)
            
        Returns:
            Preprocessed tensor
        """
        # Convert to PIL Image
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        # Apply transforms
        tensor = self.transform(image)
        
        return tensor
    
    def preprocess_batch(self, images: List[np.ndarray]) -> torch.Tensor:
        """
        Preprocess a batch of images
        
        Args:
            images: List of images
            
        Returns:
            Batch tensor
        """
        tensors = [self.preprocess_image(img) for img in images]
        batch = torch.stack(tensors)
        
        return batch


def align_face(image: np.ndarray, landmarks: dict) -> np.ndarray:
    """
    Align face using eye landmarks
    
    Args:
        image: Input image
        landmarks: Dictionary with 'left_eye' and 'right_eye' coordinates
        
    Returns:
        Aligned face image
    """
    left_eye = landmarks['left_eye']
    right_eye = landmarks['right_eye']
    
    # Calculate angle
    dY = right_eye[1] - left_eye[1]
    dX = right_eye[0] - left_eye[0]
    angle = np.degrees(np.arctan2(dY, dX))
    
    # Calculate center point between eyes
    eyes_center = ((left_eye[0] + right_eye[0]) // 2,
                   (left_eye[1] + right_eye[1]) // 2)
    
    # Get rotation matrix
    M = cv2.getRotationMatrix2D(eyes_center, angle, 1.0)
    
    # Apply rotation
    aligned = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]),
                            flags=cv2.INTER_CUBIC)
    
    return aligned


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize image to [0, 1] range
    
    Args:
        image: Input image
        
    Returns:
        Normalized image
    """
    return image.astype(np.float32) / 255.0


def denormalize_image(image: np.ndarray) -> np.ndarray:
    """
    Denormalize image from [0, 1] to [0, 255]
    
    Args:
        image: Normalized image
        
    Returns:
        Denormalized image
    """
    return (image * 255).astype(np.uint8)


def resize_image(image: np.ndarray, size: Tuple[int, int]) -> np.ndarray:
    """
    Resize image to specified size
    
    Args:
        image: Input image
        size: Target size (width, height)
        
    Returns:
        Resized image
    """
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)


def load_image_from_file(file_path: str) -> np.ndarray:
    """
    Load image from file path
    
    Args:
        file_path: Path to image file
        
    Returns:
        Image as numpy array (RGB)
    """
    image = cv2.imread(file_path)
    if image is None:
        raise ValueError(f"Failed to load image from {file_path}")
    
    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    return image


def load_image_from_bytes(image_bytes: bytes) -> np.ndarray:
    """
    Load image from bytes
    
    Args:
        image_bytes: Image data as bytes
        
    Returns:
        Image as numpy array (RGB)
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValueError("Failed to decode image from bytes")
    
    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    return image
