# NETRA Setup & Troubleshooting Guide

Complete guide for setting up NETRA globally and fixing common errors.

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Global Setup](#global-setup)
4. [Common Errors & Fixes](#common-errors--fixes)
5. [Verification](#verification)
6. [Performance Optimization](#performance-optimization)

---

## 🔧 Prerequisites

### System Requirements
- **OS**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.15+
- **Python**: 3.8, 3.9, 3.10, or 3.11
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: 5GB free space
- **GPU** (Optional): NVIDIA GPU with CUDA 11.0+ for training

### Software Requirements
```bash
# Check Python version
python --version  # Should be 3.8+

# Check pip
pip --version

# Check git
git --version
```

---

## 📦 Installation Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/your-org/NETRA-Facial-Recognition-system.git
cd NETRA-Facial-Recognition-system
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv netra-env
netra-env\Scripts\activate

# Linux/Mac
python3 -m venv netra-env
source netra-env/bin/activate
```

### Step 3: Upgrade pip
```bash
python -m pip install --upgrade pip setuptools wheel
```

### Step 4: Install Dependencies
```bash
# Install main dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

### Step 5: Create Required Directories
```bash
# Windows
mkdir models data\train data\val logs uploads

# Linux/Mac
mkdir -p models data/train data/val logs uploads
```

### Step 6: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings (optional)
```

---

## 🌍 Global Setup

### Option 1: Install as Python Package (Recommended)

```bash
# Install in editable mode
pip install -e .
```

Create `setup.py` in project root:
```python
from setuptools import setup, find_packages

setup(
    name="netra",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        line.strip() 
        for line in open('requirements.txt').readlines()
        if not line.startswith('#')
    ],
    entry_points={
        'console_scripts': [
            'netra-server=app.main:main',
            'netra-train=app.train:main',
            'netra-eval=scripts.evaluate:main',
        ],
    },
)
```

Then install:
```bash
pip install -e .
```

Now you can run from anywhere:
```bash
netra-server  # Start API server
netra-train --config configs/config.yaml  # Train model
```

### Option 2: Add to System PATH

#### Windows
```powershell
# Add to PATH temporarily
$env:PYTHONPATH = "C:\path\to\NETRA-Facial-Recognition-system;$env:PYTHONPATH"

# Add permanently (PowerShell as Admin)
[Environment]::SetEnvironmentVariable(
    "PYTHONPATH",
    "C:\path\to\NETRA-Facial-Recognition-system",
    "User"
)
```

#### Linux/Mac
```bash
# Add to ~/.bashrc or ~/.zshrc
export PYTHONPATH="/path/to/NETRA-Facial-Recognition-system:$PYTHONPATH"

# Reload
source ~/.bashrc  # or source ~/.zshrc
```

### Option 3: Docker (Truly Global)

```bash
# Build image
docker build -t netra:latest .

# Create alias (Linux/Mac)
echo 'alias netra="docker run -p 8000:8000 netra:latest"' >> ~/.bashrc
source ~/.bashrc

# Now run from anywhere
netra
```

---

## 🐛 Common Errors & Fixes

### Error 1: ModuleNotFoundError: No module named 'app'

**Cause**: Python can't find the app module

**Fix 1**: Set PYTHONPATH
```bash
# Windows
set PYTHONPATH=%CD%

# Linux/Mac
export PYTHONPATH=$(pwd)
```

**Fix 2**: Run from project root
```bash
cd /path/to/NETRA-Facial-Recognition-system
python -m app.main
```

**Fix 3**: Install as package
```bash
pip install -e .
```

---

### Error 2: ImportError: cannot import name 'SiameseNetwork'

**Cause**: Circular imports or missing __init__.py

**Fix**: Ensure all __init__.py files exist
```bash
# Create if missing
touch app/__init__.py
touch tests/__init__.py
```

---

### Error 3: FileNotFoundError: configs/config.yaml

**Cause**: Config file not found

**Fix 1**: Create config directory
```bash
mkdir -p configs
```

**Fix 2**: Use absolute path
```python
# In code
config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'config.yaml')
```

**Fix 3**: Copy from template
```bash
cp configs/config.yaml.example configs/config.yaml
```

---

### Error 4: RuntimeError: CUDA out of memory

**Cause**: GPU memory exhausted

**Fix 1**: Reduce batch size
```yaml
# configs/config.yaml
training:
  batch_size: 16  # Reduce from 32
```

**Fix 2**: Use CPU
```yaml
model:
  device: "cpu"
```

**Fix 3**: Clear GPU cache
```python
import torch
torch.cuda.empty_cache()
```

---

### Error 5: OSError: [WinError 126] The specified module could not be found

**Cause**: Missing Visual C++ Redistributables (Windows)

**Fix**: Install Visual C++ Redistributables
- Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Install and restart

---

### Error 6: No module named 'cv2'

**Cause**: OpenCV not installed properly

**Fix 1**: Reinstall opencv-python
```bash
pip uninstall opencv-python opencv-python-headless
pip install opencv-python
```

**Fix 2**: Install system dependencies (Linux)
```bash
sudo apt-get update
sudo apt-get install libgl1-mesa-glx libglib2.0-0
```

---

### Error 7: face_recognition installation fails

**Cause**: dlib compilation issues

**Fix (Windows)**:
```bash
# Install CMake
pip install cmake

# Install dlib from wheel
pip install https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp39-cp39-win_amd64.whl

# Then install face_recognition
pip install face-recognition
```

**Fix (Linux)**:
```bash
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
pip install dlib
pip install face-recognition
```

---

### Error 8: Port 8000 already in use

**Cause**: Another process using port 8000

**Fix 1**: Kill process
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**Fix 2**: Use different port
```bash
uvicorn app.main:app --port 8001
```

---

### Error 9: Permission denied (Docker)

**Cause**: Docker requires sudo

**Fix (Linux)**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Restart Docker
sudo systemctl restart docker
```

---

### Error 10: Model file not found

**Cause**: No pre-trained model

**Fix**: This is normal for first run. Options:

**Option 1**: Train your own model
```bash
python app/train.py --config configs/config.yaml
```

**Option 2**: Download pre-trained model
```bash
# Create models directory
mkdir -p models

# Download (if available)
wget https://your-server.com/models/siamese.pth -O models/siamese.pth
```

**Option 3**: Start without model (detection only)
```bash
# API will start but verification endpoints won't work
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

### Error 11: YAML parsing error

**Cause**: Invalid YAML syntax in config

**Fix**: Validate YAML
```python
import yaml

with open('configs/config.yaml', 'r') as f:
    try:
        config = yaml.safe_load(f)
        print("✓ Valid YAML")
    except yaml.YAMLError as e:
        print(f"✗ Invalid YAML: {e}")
```

---

### Error 12: Tensor size mismatch

**Cause**: Model architecture doesn't match saved weights

**Fix**: Ensure consistent configuration
```yaml
# configs/config.yaml
model:
  embedding_dim: 128  # Must match training
  backbone: "resnet50"  # Must match training
```

---

## ✅ Verification

### Test 1: Check Installation
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import cv2; print(f'OpenCV: {cv2.__version__}')"
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"
```

### Test 2: Check Imports
```bash
python -c "from app.model import SiameseNetwork; print('✓ Model import OK')"
python -c "from app.main import app; print('✓ Main import OK')"
```

### Test 3: Start Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000/docs

### Test 4: Run Tests
```bash
pytest tests/ -v
```

### Test 5: Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## 🚀 Performance Optimization

### 1. Use GPU
```yaml
# configs/config.yaml
model:
  device: "cuda"  # or "auto"
```

### 2. Optimize Batch Size
```yaml
training:
  batch_size: 32  # Adjust based on GPU memory
```

### 3. Use Smaller Backbone
```yaml
model:
  backbone: "resnet18"  # Faster than resnet50
```

### 4. Enable Multi-threading
```yaml
data:
  num_workers: 4  # Adjust based on CPU cores
```

### 5. Use Production Server
```bash
# Instead of uvicorn directly
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## 🔍 Debugging Tips

### Enable Debug Logging
```python
# app/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check GPU Usage
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device: {torch.cuda.get_device_name(0)}")
print(f"CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
```

### Profile Code
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumtime')
stats.print_stats(10)
```

---

## 📞 Getting Help

### Check Logs
```bash
# Application logs
tail -f logs/netra.log

# Docker logs
docker-compose logs -f netra-api

# Kubernetes logs
kubectl logs -f deployment/netra-deployment
```

### Report Issues
Include:
1. Error message (full traceback)
2. Python version: `python --version`
3. OS and version
4. Steps to reproduce
5. Relevant config files

### Community Support
- GitHub Issues: Report bugs
- Stack Overflow: Tag `netra-facial-recognition`
- Discord/Slack: Real-time help

---

## 🎓 Best Practices

1. **Always use virtual environment**
2. **Keep dependencies updated**: `pip install --upgrade -r requirements.txt`
3. **Use version control**: Commit changes regularly
4. **Test before deploying**: Run test suite
5. **Monitor in production**: Use Prometheus + Grafana
6. **Backup models**: Save trained models regularly
7. **Use environment variables**: Never hardcode secrets
8. **Enable logging**: Monitor application behavior
9. **Scale horizontally**: Use Kubernetes HPA
10. **Regular security updates**: Keep dependencies patched

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **File Structure**: FILE_STRUCTURE_GUIDE.md
- **API Examples**: API_EXAMPLES.md
- **Deployment Guide**: DEPLOYMENT.md
- **Quick Start**: QUICKSTART.md

---

**Last Updated**: 2025-10-06  
**Version**: 1.0.0  
**Maintainer**: NETRA Team
