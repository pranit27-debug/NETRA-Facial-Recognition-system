# NETRA Installation Guide

Complete step-by-step installation guide for all platforms.

---

## 🖥️ System Requirements

### Minimum Requirements
- **CPU**: 2 cores, 2.0 GHz
- **RAM**: 4 GB
- **Storage**: 5 GB free space
- **OS**: Windows 10+, Ubuntu 20.04+, macOS 10.15+
- **Python**: 3.8, 3.9, 3.10, or 3.11

### Recommended Requirements
- **CPU**: 4+ cores, 3.0 GHz
- **RAM**: 8+ GB
- **Storage**: 10+ GB SSD
- **GPU**: NVIDIA GPU with 4GB+ VRAM (for training)
- **Python**: 3.10

---

## 📦 Installation Methods

Choose the method that best suits your needs:

### Method 1: Quick Install (Recommended)
```bash
# Clone repository
git clone https://github.com/your-org/NETRA-Facial-Recognition-system.git
cd NETRA-Facial-Recognition-system

# Install as package
pip install -e .

# Verify installation
netra-server --help
```

### Method 2: Docker (Easiest)
```bash
# Clone repository
git clone https://github.com/your-org/NETRA-Facial-Recognition-system.git
cd NETRA-Facial-Recognition-system

# Start with Docker Compose
docker-compose up -d

# Verify
curl http://localhost:8000/health
```

### Method 3: Manual Installation
```bash
# Clone repository
git clone https://github.com/your-org/NETRA-Facial-Recognition-system.git
cd NETRA-Facial-Recognition-system

# Create virtual environment
python -m venv netra-env

# Activate (Windows)
netra-env\Scripts\activate

# Activate (Linux/Mac)
source netra-env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Set PYTHONPATH
export PYTHONPATH=$(pwd)  # Linux/Mac
set PYTHONPATH=%CD%       # Windows

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 🪟 Windows Installation

### Step 1: Install Python
1. Download Python from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

### Step 2: Install Git
1. Download from https://git-scm.com/download/win
2. Run installer with default settings

### Step 3: Install Visual C++ Redistributables
1. Download from https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Run installer

### Step 4: Clone and Install
```powershell
# Open PowerShell
cd Desktop
git clone https://github.com/your-org/NETRA-Facial-Recognition-system.git
cd NETRA-Facial-Recognition-system

# Create virtual environment
python -m venv netra-env
netra-env\Scripts\activate

# Install
pip install -e .

# Run
netra-server
```

### Step 5: Verify
Open browser: http://localhost:8000/docs

---

## 🐧 Linux Installation (Ubuntu/Debian)

### Step 1: Install Dependencies
```bash
sudo apt-get update
sudo apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    git \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-all-dev \
    libgl1-mesa-glx \
    libglib2.0-0
```

### Step 2: Clone and Install
```bash
cd ~
git clone https://github.com/your-org/NETRA-Facial-Recognition-system.git
cd NETRA-Facial-Recognition-system

# Create virtual environment
python3.10 -m venv netra-env
source netra-env/bin/activate

# Install
pip install --upgrade pip
pip install -e .

# Run
netra-server
```

### Step 3: Create Systemd Service (Optional)
```bash
sudo nano /etc/systemd/system/netra.service
```

Add:
```ini
[Unit]
Description=NETRA Facial Recognition API
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/NETRA-Facial-Recognition-system
Environment="PATH=/home/your-username/NETRA-Facial-Recognition-system/netra-env/bin"
ExecStart=/home/your-username/NETRA-Facial-Recognition-system/netra-env/bin/netra-server
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable netra
sudo systemctl start netra
sudo systemctl status netra
```

---

## 🍎 macOS Installation

### Step 1: Install Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Dependencies
```bash
brew install python@3.10 git cmake
```

### Step 3: Clone and Install
```bash
cd ~
git clone https://github.com/your-org/NETRA-Facial-Recognition-system.git
cd NETRA-Facial-Recognition-system

# Create virtual environment
python3.10 -m venv netra-env
source netra-env/bin/activate

# Install
pip install --upgrade pip
pip install -e .

# Run
netra-server
```

---

## 🐳 Docker Installation

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose

### Installation
```bash
# Clone repository
git clone https://github.com/your-org/NETRA-Facial-Recognition-system.git
cd NETRA-Facial-Recognition-system

# Build and start
docker-compose up -d

# View logs
docker-compose logs -f netra-api

# Stop
docker-compose down
```

### Access Services
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

---

## ☸️ Kubernetes Installation

### Prerequisites
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl configured

### Installation
```bash
# Clone repository
git clone https://github.com/your-org/NETRA-Facial-Recognition-system.git
cd NETRA-Facial-Recognition-system

# Create namespace
kubectl create namespace netra

# Deploy
kubectl apply -f k8s/ -n netra

# Check status
kubectl get pods -n netra
kubectl get svc -n netra

# Get service URL
kubectl get svc netra-service -n netra
```

---

## 🔧 Post-Installation Setup

### 1. Create Configuration
```bash
cp .env.example .env
nano .env  # Edit with your settings
```

### 2. Create Directories
```bash
mkdir -p models data/train data/val logs
```

### 3. Download Pre-trained Model (Optional)
```bash
# If you have a pre-trained model
wget https://your-server.com/models/siamese.pth -O models/siamese.pth
```

### 4. Verify Installation
```bash
# Check imports
python -c "from app.model import SiameseNetwork; print('✓ Model OK')"
python -c "from app.main import app; print('✓ API OK')"
python -c "import torch; print(f'✓ PyTorch {torch.__version__}')"

# Check server
curl http://localhost:8000/health
```

---

## 🧪 Testing Installation

### Run Tests
```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=app tests/
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# API documentation
curl http://localhost:8000/docs

# Test detection (with image)
curl -X POST "http://localhost:8000/api/v1/detect" \
  -F "image=@test_image.jpg"
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'app'"
**Solution**:
```bash
# Set PYTHONPATH
export PYTHONPATH=$(pwd)

# Or install as package
pip install -e .
```

### Issue: "CUDA out of memory"
**Solution**:
```yaml
# Edit configs/config.yaml
model:
  device: "cpu"  # Use CPU instead
```

### Issue: "Port 8000 already in use"
**Solution**:
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8001
```

### Issue: "face_recognition installation fails"
**Solution (Windows)**:
```bash
# Install pre-built wheel
pip install https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp310-cp310-win_amd64.whl
pip install face-recognition
```

**Solution (Linux)**:
```bash
sudo apt-get install build-essential cmake
pip install dlib
pip install face-recognition
```

---

## 🚀 Quick Start After Installation

### 1. Start Server
```bash
netra-server
# or
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Access API Documentation
Open browser: http://localhost:8000/docs

### 3. Test with Python
```python
from app.inference_client import NetraClient

client = NetraClient("http://localhost:8000")
print(client.health_check())
```

### 4. Test with cURL
```bash
curl http://localhost:8000/health
```

---

## 📚 Next Steps

1. **Read Documentation**: Check `README_ENTERPRISE.md`
2. **Train Model**: See `DEPLOYMENT.md` for training guide
3. **Configure**: Edit `configs/config.yaml`
4. **Deploy**: Follow deployment guide for production

---

## 🆘 Getting Help

- **Documentation**: See all `.md` files in project root
- **Issues**: GitHub Issues
- **Debug Report**: See `DEBUG_REPORT.md`
- **Setup Guide**: See `SETUP_AND_TROUBLESHOOTING.md`

---

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] PYTHONPATH set (if needed)
- [ ] Configuration created
- [ ] Directories created
- [ ] Server starts successfully
- [ ] Health check passes
- [ ] API docs accessible
- [ ] Tests pass

---

**Installation Complete!** 🎉

Your NETRA Facial Recognition System is now ready to use.

**Quick Commands**:
```bash
netra-server              # Start server
netra-train              # Train model
pytest tests/ -v         # Run tests
docker-compose up -d     # Start with Docker
```

Visit http://localhost:8000/docs to explore the API!
