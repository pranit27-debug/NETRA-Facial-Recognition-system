# NETRA API Examples

Complete examples for using the NETRA Facial Recognition API.

## Table of Contents
- [Health Check](#health-check)
- [Face Detection](#face-detection)
- [Face Verification](#face-verification)
- [Similarity Calculation](#similarity-calculation)
- [Python Client](#python-client)
- [JavaScript/Node.js](#javascript-examples)

## Health Check

### cURL
```bash
curl -X GET "http://localhost:8000/health"
```

### Python
```python
import requests

response = requests.get("http://localhost:8000/health")
print(response.json())
```

### Response
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda",
  "timestamp": "2024-01-15T10:30:00"
}
```

## Face Detection

Detect all faces in an image.

### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@/path/to/photo.jpg"
```

### Python
```python
import requests

url = "http://localhost:8000/api/v1/detect"
files = {"image": open("photo.jpg", "rb")}

response = requests.post(url, files=files)
result = response.json()

print(f"Found {result['face_count']} faces")
for face in result['faces']:
    print(f"Face {face['id']}: bbox={face['bbox']}, confidence={face['confidence']:.3f}")
```

### Response
```json
{
  "status": "success",
  "face_count": 2,
  "faces": [
    {
      "id": 0,
      "bbox": [100, 150, 300, 350],
      "confidence": 0.9876,
      "area": 40000
    },
    {
      "id": 1,
      "bbox": [400, 200, 550, 400],
      "confidence": 0.9654,
      "area": 30000
    }
  ]
}
```

## Face Verification

Verify if two face images belong to the same person.

### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/verify" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image1=@person1.jpg" \
  -F "image2=@person2.jpg" \
  -F "threshold=0.7"
```

### Python
```python
import requests

url = "http://localhost:8000/api/v1/verify"
files = {
    "image1": open("person1.jpg", "rb"),
    "image2": open("person2.jpg", "rb")
}
data = {"threshold": 0.7}

response = requests.post(url, files=files, data=data)
result = response.json()

if result['is_match']:
    print(f"✓ Same person (similarity: {result['similarity_score']:.4f})")
else:
    print(f"✗ Different persons (similarity: {result['similarity_score']:.4f})")
```

### Response
```json
{
  "status": "success",
  "similarity_score": 0.8943,
  "is_match": true,
  "threshold_used": 0.7
}
```

## Similarity Calculation

Calculate detailed similarity metrics between two faces.

### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/similarity" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image1=@face1.jpg" \
  -F "image2=@face2.jpg"
```

### Python
```python
import requests

url = "http://localhost:8000/api/v1/similarity"
files = {
    "image1": open("face1.jpg", "rb"),
    "image2": open("face2.jpg", "rb")
}

response = requests.post(url, files=files)
result = response.json()

print(f"Cosine Similarity: {result['cosine_similarity']:.4f}")
print(f"Euclidean Distance: {result['euclidean_distance']:.4f}")
print(f"Normalized Similarity: {result['normalized_similarity']:.4f}")
```

### Response
```json
{
  "status": "success",
  "cosine_similarity": 0.8943,
  "euclidean_distance": 0.4567,
  "normalized_similarity": 0.9471
}
```

## Python Client

Use the built-in Python client for easier integration.

```python
from app.inference_client import NetraClient

# Initialize client
client = NetraClient(base_url="http://localhost:8000")

# Health check
health = client.health_check()
print(f"API Status: {health['status']}")

# Detect faces
faces = client.detect_faces("group_photo.jpg")
print(f"Detected {faces['face_count']} faces")

# Verify faces
verification = client.verify_faces("person1.jpg", "person2.jpg", threshold=0.7)
print(f"Match: {verification['is_match']}")
print(f"Score: {verification['similarity_score']:.4f}")

# Calculate similarity
similarity = client.calculate_similarity("face1.jpg", "face2.jpg")
print(f"Cosine Similarity: {similarity['cosine_similarity']:.4f}")
```

## JavaScript Examples

### Using Fetch API
```javascript
// Detect faces
async function detectFaces(imageFile) {
  const formData = new FormData();
  formData.append('image', imageFile);

  const response = await fetch('http://localhost:8000/api/v1/detect', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  console.log(`Found ${result.face_count} faces`);
  return result;
}

// Verify faces
async function verifyFaces(image1, image2, threshold = 0.7) {
  const formData = new FormData();
  formData.append('image1', image1);
  formData.append('image2', image2);
  formData.append('threshold', threshold);

  const response = await fetch('http://localhost:8000/api/v1/verify', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  console.log(`Match: ${result.is_match}, Score: ${result.similarity_score}`);
  return result;
}
```

### Using Axios
```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

// Detect faces
async function detectFaces(imagePath) {
  const form = new FormData();
  form.append('image', fs.createReadStream(imagePath));

  const response = await axios.post(
    'http://localhost:8000/api/v1/detect',
    form,
    { headers: form.getHeaders() }
  );

  return response.data;
}

// Verify faces
async function verifyFaces(imagePath1, imagePath2) {
  const form = new FormData();
  form.append('image1', fs.createReadStream(imagePath1));
  form.append('image2', fs.createReadStream(imagePath2));
  form.append('threshold', '0.7');

  const response = await axios.post(
    'http://localhost:8000/api/v1/verify',
    form,
    { headers: form.getHeaders() }
  );

  return response.data;
}
```

## Batch Processing

Process multiple images efficiently.

### Python
```python
import requests
from concurrent.futures import ThreadPoolExecutor
import os

def process_image(image_path):
    url = "http://localhost:8000/api/v1/detect"
    with open(image_path, 'rb') as f:
        files = {"image": f}
        response = requests.post(url, files=files)
        return response.json()

# Process multiple images in parallel
image_dir = "images/"
image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir)]

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(process_image, image_files))

for img, result in zip(image_files, results):
    print(f"{img}: {result['face_count']} faces detected")
```

## Error Handling

### Python
```python
import requests

def safe_verify(image1_path, image2_path):
    try:
        url = "http://localhost:8000/api/v1/verify"
        files = {
            "image1": open(image1_path, "rb"),
            "image2": open(image2_path, "rb")
        }
        
        response = requests.post(url, files=files, timeout=30)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.ConnectionError:
        print("Could not connect to API")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    
    return None
```

## Rate Limiting

The API has rate limiting enabled (default: 100 requests/minute).

### Handle Rate Limiting
```python
import requests
import time

def call_api_with_retry(url, files, max_retries=3):
    for attempt in range(max_retries):
        response = requests.post(url, files=files)
        
        if response.status_code == 429:  # Too Many Requests
            wait_time = int(response.headers.get('Retry-After', 60))
            print(f"Rate limited. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            continue
        
        return response.json()
    
    raise Exception("Max retries exceeded")
```

## Complete Example Application

```python
#!/usr/bin/env python3
"""
Complete example application using NETRA API
"""

import argparse
from app.inference_client import NetraClient

def main():
    parser = argparse.ArgumentParser(description='NETRA Face Recognition Demo')
    parser.add_argument('action', choices=['detect', 'verify', 'similarity'])
    parser.add_argument('--image1', required=True)
    parser.add_argument('--image2')
    parser.add_argument('--threshold', type=float, default=0.7)
    parser.add_argument('--url', default='http://localhost:8000')
    
    args = parser.parse_args()
    
    client = NetraClient(base_url=args.url)
    
    if args.action == 'detect':
        result = client.detect_faces(args.image1)
        print(f"\n✓ Detected {result['face_count']} face(s):")
        for face in result['faces']:
            print(f"  - Face {face['id']}: confidence={face['confidence']:.3f}")
    
    elif args.action == 'verify':
        if not args.image2:
            print("Error: --image2 required for verify")
            return
        
        result = client.verify_faces(args.image1, args.image2, args.threshold)
        
        if result['is_match']:
            print(f"\n✓ MATCH (score: {result['similarity_score']:.4f})")
        else:
            print(f"\n✗ NO MATCH (score: {result['similarity_score']:.4f})")
    
    elif args.action == 'similarity':
        if not args.image2:
            print("Error: --image2 required for similarity")
            return
        
        result = client.calculate_similarity(args.image1, args.image2)
        print(f"\n📊 Similarity Metrics:")
        print(f"  Cosine Similarity: {result['cosine_similarity']:.4f}")
        print(f"  Euclidean Distance: {result['euclidean_distance']:.4f}")

if __name__ == "__main__":
    main()
```

Run it:
```bash
python demo.py detect --image1 photo.jpg
python demo.py verify --image1 person1.jpg --image2 person2.jpg
python demo.py similarity --image1 face1.jpg --image2 face2.jpg
```
