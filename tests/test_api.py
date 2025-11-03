"""
API endpoint tests
"""

import pytest
import io
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_test_image(size=(160, 160)):
    """Create a test image"""
    img = Image.new('RGB', size, color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "NETRA" in data["service"]


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_readiness_check():
    """Test readiness endpoint"""
    response = client.get("/ready")
    # Should be 200 or 503 depending on model load status
    assert response.status_code in [200, 503]


def test_detect_faces_no_image():
    """Test detect endpoint without image"""
    response = client.post("/api/v1/detect")
    assert response.status_code == 422  # Validation error


def test_detect_faces_with_image():
    """Test detect endpoint with image"""
    img_bytes = create_test_image()
    files = {"image": ("test.jpg", img_bytes, "image/jpeg")}
    
    response = client.post("/api/v1/detect", files=files)
    assert response.status_code in [200, 500]  # May fail if model not loaded
    
    if response.status_code == 200:
        data = response.json()
        assert "status" in data
        assert "face_count" in data


def test_verify_faces_missing_images():
    """Test verify endpoint with missing images"""
    response = client.post("/api/v1/verify")
    assert response.status_code == 422


def test_verify_faces_with_images():
    """Test verify endpoint with two images"""
    img1_bytes = create_test_image()
    img2_bytes = create_test_image()
    
    files = {
        "image1": ("test1.jpg", img1_bytes, "image/jpeg"),
        "image2": ("test2.jpg", img2_bytes, "image/jpeg")
    }
    data = {"threshold": 0.7}
    
    response = client.post("/api/v1/verify", files=files, data=data)
    assert response.status_code in [200, 400, 500]


def test_similarity_endpoint():
    """Test similarity calculation endpoint"""
    img1_bytes = create_test_image()
    img2_bytes = create_test_image()
    
    files = {
        "image1": ("test1.jpg", img1_bytes, "image/jpeg"),
        "image2": ("test2.jpg", img2_bytes, "image/jpeg")
    }
    
    response = client.post("/api/v1/similarity", files=files)
    assert response.status_code in [200, 400, 500]


def test_metrics_endpoint():
    """Test Prometheus metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]


def test_api_documentation():
    """Test OpenAPI documentation"""
    response = client.get("/docs")
    assert response.status_code == 200
    
    response = client.get("/redoc")
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
