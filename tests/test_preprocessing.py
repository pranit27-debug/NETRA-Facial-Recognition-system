"""
Tests for preprocessing utilities
"""

import pytest
import numpy as np
from PIL import Image
from app.preprocess import (
    FaceDetector, ImagePreprocessor,
    normalize_image, denormalize_image,
    resize_image
)


def create_test_image_array(size=(160, 160)):
    """Create a test image as numpy array"""
    img = Image.new('RGB', size, color='blue')
    return np.array(img)


def test_face_detector_initialization():
    """Test FaceDetector initialization"""
    detector = FaceDetector()
    assert detector is not None
    assert detector.detector is not None


def test_image_preprocessor_initialization():
    """Test ImagePreprocessor initialization"""
    preprocessor = ImagePreprocessor(image_size=160)
    assert preprocessor is not None
    assert preprocessor.image_size == 160


def test_preprocess_image():
    """Test image preprocessing"""
    preprocessor = ImagePreprocessor(image_size=160)
    img_array = create_test_image_array((200, 200))
    
    tensor = preprocessor.preprocess_image(img_array)
    
    assert tensor.shape == (3, 160, 160)
    assert tensor.dtype == np.float32 or str(tensor.dtype) == 'torch.float32'


def test_normalize_image():
    """Test image normalization"""
    img = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    normalized = normalize_image(img)
    
    assert normalized.dtype == np.float32
    assert normalized.min() >= 0
    assert normalized.max() <= 1


def test_denormalize_image():
    """Test image denormalization"""
    img = np.random.rand(100, 100, 3).astype(np.float32)
    denormalized = denormalize_image(img)
    
    assert denormalized.dtype == np.uint8
    assert denormalized.min() >= 0
    assert denormalized.max() <= 255


def test_resize_image():
    """Test image resizing"""
    img = create_test_image_array((200, 200))
    resized = resize_image(img, (100, 100))
    
    assert resized.shape[:2] == (100, 100)


def test_normalize_denormalize_roundtrip():
    """Test normalization and denormalization roundtrip"""
    original = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)
    normalized = normalize_image(original)
    restored = denormalize_image(normalized)
    
    # Should be approximately equal (allowing for rounding errors)
    assert np.allclose(original, restored, atol=1)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
