# NETRA File Structure & Explanation Guide

Complete guide to understanding every file in the NETRA Facial Recognition System.

## 📁 Project Structure Overview

```
NETRA-Facial-Recognition-system/
├── app/                          # Core application code
├── configs/                      # Configuration files
├── k8s/                         # Kubernetes manifests
├── monitoring/                   # Monitoring configs
├── scripts/                      # Utility scripts
├── tests/                       # Test suite
├── data/                        # Training data (gitignored)
├── models/                      # Saved models (gitignored)
├── logs/                        # Application logs (gitignored)
└── [Configuration & Documentation files]
```

---

## 🔧 Core Application Files (`app/`)

### 1. `app/__init__.py`
**Purpose**: Package initialization file  
**Content**: Version info and package metadata  
**Usage**: Makes `app` a Python package

```python
__version__ = "1.0.0"
__author__ = "NETRA Team"
```

---

### 2. `app/main.py` ⭐ **MAIN APPLICATION**
**Purpose**: FastAPI application entry point  
**Key Components**:
- **FastAPI App**: REST API server with OpenAPI docs
- **CORS Middleware**: Cross-origin resource sharing
- **Prometheus Metrics**: Performance monitoring
- **Startup Event**: Loads model and initializes services

**Endpoints**:
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /ready` - Readiness probe (Kubernetes)
- `POST /api/v1/detect` - Detect faces in image
- `POST /api/v1/verify` - Verify if two faces match
- `POST /api/v1/similarity` - Calculate similarity metrics
- `GET /metrics` - Prometheus metrics

**How it works**:
1. On startup, loads configuration from `configs/config.yaml`
2. Initializes face detector (MTCNN)
3. Loads pre-trained Siamese model
4. Exposes REST API endpoints
5. Processes images and returns results

**Run it**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

### 3. `app/model.py` 🧠 **NEURAL NETWORK**
**Purpose**: Siamese Neural Network implementation  
**Key Classes**:

#### `SiameseNetwork`
- **Architecture**: ResNet backbone + embedding layer
- **Input**: Two images (224x224x3)
- **Output**: Two 128-dimensional embeddings
- **Features**: 
  - Shared weights between branches
  - L2 normalized embeddings
  - Supports ResNet18 and ResNet50 backbones

#### `ContrastiveLoss`
- **Purpose**: Training loss function
- **Formula**: Pulls same-person pairs together, pushes different pairs apart
- **Margin**: Configurable distance threshold

#### Helper Functions
- `cosine_similarity()`: Calculate similarity (0-1)
- `euclidean_distance()`: Calculate distance

**How it works**:
```
Image 1 → CNN Backbone → Embedding → 
                                      → Distance → Similarity Score
Image 2 → CNN Backbone → Embedding →
         (Shared Weights)
```

---

### 4. `app/dataset.py` 📊 **DATA LOADING**
**Purpose**: Dataset preparation and loading  
**Key Classes**:

#### `SiameseDataset`
- **Input**: Directory with person folders
- **Output**: Image pairs with labels (1=same, 0=different)
- **Features**:
  - Automatic pair generation
  - Balanced positive/negative samples
  - Supports multiple images per person

#### Functions
- `get_transforms()`: Image augmentation pipeline
- `create_dataloaders()`: Creates train/val loaders

**Data Structure Expected**:
```
data/
├── train/
│   ├── person1/
│   │   ├── img1.jpg
│   │   └── img2.jpg
│   └── person2/
│       └── img1.jpg
└── val/
    └── ...
```

---

### 5. `app/preprocess.py` 🖼️ **IMAGE PROCESSING**
**Purpose**: Image preprocessing and face detection  
**Key Classes**:

#### `FaceDetector`
- **Technology**: MTCNN (Multi-task Cascaded CNN)
- **Features**: 
  - Detects multiple faces
  - Returns bounding boxes
  - Provides confidence scores
  - Extracts facial landmarks

#### `ImagePreprocessor`
- **Operations**:
  - Resize to target size (160x160)
  - Normalize (ImageNet mean/std)
  - Convert to tensor
  - Batch processing

#### Helper Functions
- `align_face()`: Align face using eye landmarks
- `normalize_image()`: Scale to [0,1]
- `load_image_from_bytes()`: Load from uploaded file

---

### 6. `app/train.py` 🎓 **TRAINING PIPELINE**
**Purpose**: Model training script  
**Features**:
- **Training Loop**: Epoch-based training
- **Validation**: Automatic validation after each epoch
- **Metrics**: Loss, accuracy, optimal threshold
- **Logging**: TensorBoard integration
- **Checkpointing**: Saves best models
- **Learning Rate Scheduling**: ReduceLROnPlateau

**Usage**:
```bash
python app/train.py --config configs/config.yaml --epochs 100
```

**Training Process**:
1. Load datasets
2. Initialize model
3. For each epoch:
   - Train on training set
   - Validate on validation set
   - Update learning rate
   - Save best model
4. Export final model

---

### 7. `app/utils.py` 🛠️ **UTILITIES**
**Purpose**: Helper functions and utilities  
**Key Functions**:

- `load_config()`: Load YAML configuration
- `get_device()`: Auto-detect GPU/CPU
- `save_model()`: Save model checkpoint
- `load_model()`: Load model checkpoint
- `count_parameters()`: Count model parameters
- `AverageMeter`: Track running averages
- `calculate_accuracy()`: Compute accuracy
- `find_optimal_threshold()`: Find best threshold

---

### 8. `app/inference_client.py` 🔌 **API CLIENT**
**Purpose**: Python client for easy API usage  
**Class**: `NetraClient`

**Methods**:
- `health_check()`: Check API status
- `detect_faces()`: Detect faces in image
- `verify_faces()`: Verify two faces
- `calculate_similarity()`: Get similarity metrics

**Usage**:
```python
from app.inference_client import NetraClient

client = NetraClient("http://localhost:8000")
result = client.verify_faces("img1.jpg", "img2.jpg")
```

---

## ⚙️ Configuration Files

### `configs/config.yaml` 📝
**Purpose**: Central configuration file  
**Sections**:
- **app**: Server settings (host, port, workers)
- **model**: Model parameters (path, backbone, device)
- **training**: Training hyperparameters
- **data**: Dataset paths and settings
- **inference**: Inference settings
- **security**: Security configurations
- **monitoring**: Logging and metrics

**Example**:
```yaml
model:
  path: "models/siamese.pth"
  embedding_dim: 128
  backbone: "resnet50"
  device: "auto"
```

---

## 🐳 Docker Files

### `Dockerfile` 🐋
**Purpose**: Container image definition  
**Features**:
- **Multi-stage build**: Optimized image size
- **Builder stage**: Compiles dependencies
- **Final stage**: Runtime environment only
- **Health check**: Built-in health monitoring
- **Entrypoint**: Automatic startup script

**Build**:
```bash
docker build -t netra:latest .
```

---

### `docker-compose.yml` 🎼
**Purpose**: Multi-container orchestration  
**Services**:
1. **netra-api**: Main application
2. **prometheus**: Metrics collection
3. **grafana**: Metrics visualization

**Run**:
```bash
docker-compose up -d
```

**Access**:
- API: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

---

### `.dockerignore` 🚫
**Purpose**: Exclude files from Docker build  
**Excludes**: Tests, docs, git, data, logs, cache

---

## ☸️ Kubernetes Files (`k8s/`)

### `k8s/deployment.yaml` 🚀
**Purpose**: Application deployment  
**Features**:
- **Replicas**: 3 pods for high availability
- **Resources**: CPU/memory limits
- **Probes**: Liveness and readiness checks
- **Volumes**: Persistent storage for models

---

### `k8s/service.yaml` 🌐
**Purpose**: Network service  
**Types**:
- **LoadBalancer**: External access
- **ClusterIP**: Internal access

---

### `k8s/ingress.yaml` 🚪
**Purpose**: HTTP routing and SSL  
**Features**:
- HTTPS redirect
- Rate limiting
- Domain routing
- SSL/TLS termination

---

### `k8s/configmap.yaml` 📋
**Purpose**: Configuration management  
**Contains**: Application config as Kubernetes ConfigMap

---

### `k8s/hpa.yaml` 📈
**Purpose**: Horizontal Pod Autoscaler  
**Features**:
- Auto-scale 2-10 pods
- CPU-based scaling (70%)
- Memory-based scaling (80%)

**Deploy all**:
```bash
kubectl apply -f k8s/
```

---

## 📊 Monitoring Files (`monitoring/`)

### `monitoring/prometheus.yml` 📉
**Purpose**: Prometheus configuration  
**Scrapes**: API metrics every 10 seconds

---

### `monitoring/grafana-dashboard.json` 📊
**Purpose**: Pre-configured Grafana dashboard  
**Metrics**:
- Request rate
- Response time
- Error rate
- CPU/Memory usage

---

## 🧪 Test Files (`tests/`)

### `tests/test_model.py` 🧠
**Tests**: Neural network functionality
- Model initialization
- Forward pass
- Loss calculation
- Similarity metrics

---

### `tests/test_api.py` 🌐
**Tests**: API endpoints
- Health checks
- Face detection
- Face verification
- Error handling

---

### `tests/test_preprocessing.py` 🖼️
**Tests**: Image preprocessing
- Face detection
- Image normalization
- Resizing

**Run tests**:
```bash
pytest tests/ -v
```

---

## 📜 Scripts (`scripts/`)

### `scripts/entrypoint.sh` 🚀
**Purpose**: Docker container startup script  
**Actions**:
- Creates directories
- Checks for model file
- Starts uvicorn server

---

### `scripts/evaluate.py` 📊
**Purpose**: Model evaluation script  
**Outputs**:
- Accuracy, precision, recall, F1
- ROC curve
- Distance distribution plots
- Optimal threshold

**Run**:
```bash
python scripts/evaluate.py --config configs/config.yaml
```

---

## 📚 Documentation Files

### `README.md` 📖
**Purpose**: Main project documentation  
**Audience**: General users

---

### `README_ENTERPRISE.md` 🏢
**Purpose**: Enterprise-grade documentation  
**Includes**: Architecture diagrams, deployment guides

---

### `DEPLOYMENT.md` 🚀
**Purpose**: Deployment instructions  
**Covers**: Local, Docker, Kubernetes

---

### `QUICKSTART.md` ⚡
**Purpose**: 5-minute quick start guide

---

### `API_EXAMPLES.md` 💻
**Purpose**: Complete API usage examples  
**Languages**: Python, JavaScript, cURL

---

### `FILE_STRUCTURE_GUIDE.md` 📁
**Purpose**: This file - explains all files

---

## 🔧 Configuration Files (Root)

### `requirements.txt` 📦
**Purpose**: Python dependencies  
**Includes**: PyTorch, FastAPI, OpenCV, etc.

**Install**:
```bash
pip install -r requirements.txt
```

---

### `requirements-dev.txt` 🛠️
**Purpose**: Development dependencies  
**Includes**: pytest, black, flake8, mypy

---

### `.env.example` 🔐
**Purpose**: Environment variables template  
**Usage**: Copy to `.env` and customize

---

### `pyproject.toml` ⚙️
**Purpose**: Python project configuration  
**Configures**: black, isort, mypy, pytest

---

### `.pre-commit-config.yaml` ✅
**Purpose**: Git pre-commit hooks  
**Runs**: Code formatting, linting before commit

**Setup**:
```bash
pre-commit install
```

---

### `.gitignore` 🚫
**Purpose**: Exclude files from git  
**Excludes**: Cache, logs, models, data, env

---

### `.gitattributes` 📝
**Purpose**: Git file handling rules  
**Defines**: Line endings, binary files

---

### `Makefile` 🔨
**Purpose**: Development automation  
**Commands**:
```bash
make install      # Install dependencies
make test         # Run tests
make docker-build # Build Docker image
make k8s-deploy   # Deploy to Kubernetes
```

---

### `LICENSE` ⚖️
**Purpose**: Software license (Apache 2.0)

---

### `CONTRIBUTING.md` 🤝
**Purpose**: Contribution guidelines

---

## 📊 Data Directories (Created at Runtime)

### `data/` 💾
**Purpose**: Training and validation datasets  
**Structure**:
```
data/
├── train/
│   └── person_name/
│       └── *.jpg
└── val/
    └── person_name/
        └── *.jpg
```

---

### `models/` 🧠
**Purpose**: Saved model checkpoints  
**Files**: `siamese.pth`, `siamese_best_acc.pth`

---

### `logs/` 📝
**Purpose**: Application and training logs  
**Files**: `netra.log`, TensorBoard logs

---

### `uploads/` 📤
**Purpose**: Temporary uploaded files (auto-cleaned)

---

## 🎯 Key File Interactions

### Training Flow
```
data/ → dataset.py → train.py → models/siamese.pth
                  ↓
              TensorBoard logs/
```

### Inference Flow
```
Image Upload → main.py → preprocess.py → model.py → Response
                      ↓
                 prometheus metrics
```

### Deployment Flow
```
Dockerfile → docker-compose.yml → Docker containers
                                ↓
                         Prometheus + Grafana

k8s/*.yaml → kubectl apply → Kubernetes cluster
```

---

## 🚀 Quick Reference

### Start Development Server
```bash
uvicorn app.main:app --reload
```

### Train Model
```bash
python app/train.py --config configs/config.yaml
```

### Run Tests
```bash
pytest tests/ -v
```

### Build Docker
```bash
docker-compose up -d
```

### Deploy Kubernetes
```bash
kubectl apply -f k8s/
```

---

## 🔍 Troubleshooting

### Import Errors
- Ensure `PYTHONPATH` includes project root
- Install all requirements: `pip install -r requirements.txt`

### Model Not Loading
- Check `models/siamese.pth` exists
- Verify path in `configs/config.yaml`

### Port Already in Use
- Change port in `configs/config.yaml`
- Or kill process: `lsof -ti:8000 | xargs kill`

### Out of Memory
- Reduce batch size in config
- Use smaller backbone (resnet18)
- Use CPU instead of GPU

---

## 📞 Support

- **Documentation**: See README files
- **API Docs**: http://localhost:8000/docs
- **Issues**: GitHub Issues
- **Examples**: API_EXAMPLES.md

---

**Last Updated**: 2025-10-06  
**Version**: 1.0.0  
**Maintainer**: NETRA Team
