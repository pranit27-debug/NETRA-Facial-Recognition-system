# NETRA Quick Start Guide

Get NETRA running in 5 minutes!

## Option 1: Docker (Recommended)

```bash
# 1. Clone and navigate
git clone <repository-url>
cd NETRA-Facial-Recognition-system

# 2. Start with Docker Compose
docker-compose up -d

# 3. Test the API
curl http://localhost:8000/health
```

✅ Done! API running at `http://localhost:8000`

## Option 2: Local Python

```bash
# 1. Clone repository
git clone <repository-url>
cd NETRA-Facial-Recognition-system

# 2. Create virtual environment
python -m venv netra-env
source netra-env/bin/activate  # Windows: netra-env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ Done! API running at `http://localhost:8000`

## Test the API

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Detect faces
curl -X POST "http://localhost:8000/api/v1/detect" \
  -F "image=@your_photo.jpg"

# Verify two faces
curl -X POST "http://localhost:8000/api/v1/verify" \
  -F "image1=@person1.jpg" \
  -F "image2=@person2.jpg" \
  -F "threshold=0.7"
```

### Using Python Client

```python
from app.inference_client import NetraClient

client = NetraClient("http://localhost:8000")

# Health check
print(client.health_check())

# Detect faces
result = client.detect_faces("photo.jpg")
print(f"Found {result['face_count']} faces")

# Verify faces
result = client.verify_faces("person1.jpg", "person2.jpg")
print(f"Match: {result['is_match']}, Score: {result['similarity_score']}")
```

### Using API Documentation

Open browser: `http://localhost:8000/docs`

Interactive API documentation with "Try it out" buttons!

## Next Steps

1. **Train custom model**: See [DEPLOYMENT.md](DEPLOYMENT.md#model-training)
2. **Deploy to production**: See [DEPLOYMENT.md](DEPLOYMENT.md#kubernetes-deployment)
3. **Monitor metrics**: Access Grafana at `http://localhost:3000`

## Need Help?

- 📚 Full docs: `README_ENTERPRISE.md`
- 🐛 Report issues: GitHub Issues
- 💬 Community: Discord/Slack
