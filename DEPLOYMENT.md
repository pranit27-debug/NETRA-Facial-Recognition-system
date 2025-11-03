# NETRA Deployment Guide

## 📦 Prerequisites

- Python 3.8+
- Docker & Docker Compose
- Kubernetes cluster (for production)
- 4GB+ RAM
- GPU (optional, for training)

## 🚀 Quick Start

### 1. Local Development

```bash
# Clone repository
git clone <repository-url>
cd NETRA-Facial-Recognition-system

# Create virtual environment
python -m venv netra-env
source netra-env/bin/activate  # Windows: netra-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Access the API at: `http://localhost:8000`  
API Documentation: `http://localhost:8000/docs`

### 2. Docker Deployment

```bash
# Build image
docker build -t netra-facial-recognition:latest .

# Run with Docker Compose (includes Prometheus & Grafana)
docker-compose up -d

# Check logs
docker-compose logs -f netra-api

# Stop services
docker-compose down
```

**Services:**
- API: `http://localhost:8000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (admin/admin)

### 3. Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace netra

# Deploy ConfigMap
kubectl apply -f k8s/configmap.yaml -n netra

# Deploy application
kubectl apply -f k8s/deployment.yaml -n netra
kubectl apply -f k8s/service.yaml -n netra

# Deploy Ingress (optional)
kubectl apply -f k8s/ingress.yaml -n netra

# Deploy HPA for autoscaling
kubectl apply -f k8s/hpa.yaml -n netra

# Check status
kubectl get pods -n netra -l app=netra
kubectl get svc -n netra
```

### 4. Model Training

```bash
# Prepare dataset
mkdir -p data/train data/val

# Organize data in folders
# data/train/person1/*.jpg
# data/train/person2/*.jpg
# ...

# Train model
python app/train.py --config configs/config.yaml --epochs 100

# Evaluate model
python scripts/evaluate.py --config configs/config.yaml
```

## 🔧 Configuration

Edit `configs/config.yaml`:

```yaml
app:
  host: "0.0.0.0"
  port: 8000

model:
  path: "models/siamese.pth"
  embedding_dim: 128
  backbone: "resnet50"
  device: "auto"
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_model.py -v
```

## 📊 Monitoring

### Prometheus Metrics

Access: `http://localhost:9090`

Key metrics:
- `http_requests_total`
- `http_request_duration_seconds`
- `process_cpu_seconds_total`
- `process_resident_memory_bytes`

### Grafana Dashboard

Access: `http://localhost:3000`
- Username: `admin`
- Password: `admin`

Import dashboard from `monitoring/grafana-dashboard.json`

## 🔒 Security Considerations

1. **Change default passwords**
2. **Use HTTPS in production**
3. **Set environment variables securely**
4. **Enable rate limiting**
5. **Regular security updates**

## 🐛 Troubleshooting

### Model not loading
- Check `models/siamese.pth` exists
- Verify model path in config
- Check logs for errors

### Out of memory
- Reduce batch size
- Use smaller backbone (resnet18)
- Add more RAM or use GPU

### API not responding
- Check port availability
- Verify firewall settings
- Check container logs

## 📚 Additional Resources

- API Documentation: `/docs`
- Health Check: `/health`
- Metrics: `/metrics`
- GitHub Issues: Report bugs

## 🔄 Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild Docker image
docker-compose build --no-cache

# Restart services
docker-compose up -d
```
