#!/usr/bin/env python3
"""
NETRA Installation Validation Script
Run this script to verify your installation is correct
"""

import sys
import subprocess
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_python_version():
    """Check Python version"""
    print("✓ Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        return False

def check_imports():
    """Check critical imports"""
    print("\n✓ Checking critical imports...")
    
    imports = {
        'torch': 'PyTorch',
        'torchvision': 'TorchVision',
        'cv2': 'OpenCV',
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'numpy': 'NumPy',
        'PIL': 'Pillow',
        'yaml': 'PyYAML',
        'mtcnn': 'MTCNN',
    }
    
    all_ok = True
    for module, name in imports.items():
        try:
            __import__(module)
            print(f"  ✅ {name} - OK")
        except ImportError:
            print(f"  ❌ {name} - MISSING")
            all_ok = False
    
    return all_ok

def check_app_imports():
    """Check app module imports"""
    print("\n✓ Checking app module imports...")
    
    modules = [
        ('app.model', 'SiameseNetwork'),
        ('app.dataset', 'SiameseDataset'),
        ('app.preprocess', 'FaceDetector'),
        ('app.utils', 'load_config'),
        ('app.main', 'app'),
    ]
    
    all_ok = True
    for module, component in modules:
        try:
            mod = __import__(module, fromlist=[component])
            getattr(mod, component)
            print(f"  ✅ {module}.{component} - OK")
        except Exception as e:
            print(f"  ❌ {module}.{component} - FAILED: {e}")
            all_ok = False
    
    return all_ok

def check_directories():
    """Check required directories"""
    print("\n✓ Checking directories...")
    
    dirs = [
        'app',
        'configs',
        'tests',
        'scripts',
        'k8s',
        'monitoring',
    ]
    
    all_ok = True
    for dir_name in dirs:
        path = Path(dir_name)
        if path.exists() and path.is_dir():
            print(f"  ✅ {dir_name}/ - OK")
        else:
            print(f"  ❌ {dir_name}/ - MISSING")
            all_ok = False
    
    return all_ok

def check_files():
    """Check required files"""
    print("\n✓ Checking required files...")
    
    files = [
        'requirements.txt',
        'setup.py',
        'Dockerfile',
        'docker-compose.yml',
        'configs/config.yaml',
        'app/main.py',
        'app/model.py',
    ]
    
    all_ok = True
    for file_name in files:
        path = Path(file_name)
        if path.exists() and path.is_file():
            print(f"  ✅ {file_name} - OK")
        else:
            print(f"  ❌ {file_name} - MISSING")
            all_ok = False
    
    return all_ok

def check_gpu():
    """Check GPU availability"""
    print("\n✓ Checking GPU...")
    
    try:
        import torch
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"  ✅ GPU Available: {device_name}")
            print(f"     Memory: {memory:.2f} GB")
            return True
        else:
            print(f"  ⚠️  No GPU detected - Will use CPU")
            return True
    except Exception as e:
        print(f"  ❌ GPU check failed: {e}")
        return False

def check_config():
    """Check configuration file"""
    print("\n✓ Checking configuration...")
    
    try:
        import yaml
        with open('configs/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        required_keys = ['app', 'model', 'training', 'data']
        all_ok = True
        
        for key in required_keys:
            if key in config:
                print(f"  ✅ config.{key} - OK")
            else:
                print(f"  ❌ config.{key} - MISSING")
                all_ok = False
        
        return all_ok
    except Exception as e:
        print(f"  ❌ Config check failed: {e}")
        return False

def run_quick_test():
    """Run a quick functionality test"""
    print("\n✓ Running quick functionality test...")
    
    try:
        from app.model import SiameseNetwork
        import torch
        
        # Create model
        model = SiameseNetwork(embedding_dim=128, backbone='resnet18')
        print(f"  ✅ Model creation - OK")
        
        # Test forward pass
        x1 = torch.randn(1, 3, 160, 160)
        x2 = torch.randn(1, 3, 160, 160)
        
        model.eval()
        with torch.no_grad():
            out1, out2 = model(x1, x2)
        
        print(f"  ✅ Forward pass - OK")
        print(f"     Output shape: {out1.shape}")
        
        return True
    except Exception as e:
        print(f"  ❌ Functionality test failed: {e}")
        return False

def main():
    """Main validation function"""
    print_header("NETRA Installation Validation")
    
    results = {
        'Python Version': check_python_version(),
        'Critical Imports': check_imports(),
        'App Imports': check_app_imports(),
        'Directories': check_directories(),
        'Files': check_files(),
        'GPU': check_gpu(),
        'Configuration': check_config(),
        'Functionality': run_quick_test(),
    }
    
    print_header("Validation Summary")
    
    passed = sum(results.values())
    total = len(results)
    
    for check, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {check:.<40} {status}")
    
    print(f"\n  Score: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n  🎉 All checks passed! Installation is valid.")
        print("\n  Next steps:")
        print("    1. Start server: netra-server")
        print("    2. Visit: http://localhost:8000/docs")
        print("    3. Run tests: pytest tests/ -v")
        return 0
    else:
        print("\n  ⚠️  Some checks failed. Please review errors above.")
        print("\n  Troubleshooting:")
        print("    1. Install dependencies: pip install -r requirements.txt")
        print("    2. Set PYTHONPATH: export PYTHONPATH=$(pwd)")
        print("    3. Install package: pip install -e .")
        print("    4. See SETUP_AND_TROUBLESHOOTING.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
