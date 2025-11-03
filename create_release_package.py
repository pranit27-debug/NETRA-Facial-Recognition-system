#!/usr/bin/env python3
"""
NETRA Project Release Package Creator
Creates a complete ZIP package of the project ready for distribution
"""

import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def create_release_package():
    """Create a complete release package"""

    print_header("NETRA Project Package Creator")

    # Get project root
    project_root = Path.cwd()
    project_name = "NETRA-Facial-Recognition-System"

    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Output filename
    output_dir = project_root.parent
    zip_filename = f"{project_name}_v1.0.0_{timestamp}.zip"
    zip_path = output_dir / zip_filename

    print(f"📦 Creating package: {zip_filename}")
    print(f"📍 Output location: {output_dir}\n")

    # Files and directories to include
    include_patterns = [
        # Core application
        'app/**/*.py',
        'app/__init__.py',

        # Configuration
        'configs/**/*.yaml',
        'configs/**/*.yml',

        # Kubernetes
        'k8s/**/*.yaml',

        # Monitoring
        'monitoring/**/*.yml',
        'monitoring/**/*.json',

        # Scripts
        'scripts/**/*.py',
        'scripts/**/*.sh',

        # Tests
        'tests/**/*.py',

        # Documentation
        '*.md',

        # Configuration files
        'requirements.txt',
        'requirements-dev.txt',
        'setup.py',
        'pyproject.toml',
        '.env.example',
        '.gitignore',
        '.gitattributes',
        '.dockerignore',
        '.pre-commit-config.yaml',

        # Docker
        'Dockerfile',
        'docker-compose.yml',
        'docker-compose.test.yml',

        # Build tools
        'Makefile',

        # Validation
        'validate_installation.py',
        'create_release_package.py',

        # License
        'LICENSE',
        'CONTRIBUTING.md',
    ]

    # Directories to exclude
    exclude_dirs = {
        '__pycache__',
        '.git',
        '.github',
        'netra-env',
        'venv',
        'env',
        '.venv',
        'node_modules',
        '.pytest_cache',
        '.mypy_cache',
        'htmlcov',
        '.tox',
        'dist',
        'build',
        '*.egg-info',
        'logs',
        'uploads',
        'models',
        'data',
        'dataset',
    }

    # Create ZIP file
    files_added = 0

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:

        print("📁 Adding files to package...\n")

        # Walk through project directory
        for root, dirs, files in os.walk(project_root):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]

            # Get relative path
            rel_root = Path(root).relative_to(project_root)

            # Skip if in excluded directory
            if any(excluded in str(rel_root) for excluded in exclude_dirs):
                continue

            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(project_root)

                # Skip excluded files
                if file.endswith('.pyc') or file.endswith('.pyo'):
                    continue
                if file.startswith('.') and file not in ['.env.example', '.gitignore', '.gitattributes', '.dockerignore', '.pre-commit-config.yaml']:
                    continue

                # Add to ZIP with project name as root folder
                arcname = Path(project_name) / rel_path
                zipf.write(file_path, arcname)
                files_added += 1

                # Print progress
                if files_added % 10 == 0:
                    print(f"  ✓ Added {files_added} files...")

        # Create README for the package
        readme_content = f"""# NETRA Facial Recognition System - Release Package

**Version**: 1.0.0
**Release Date**: {datetime.now().strftime("%Y-%m-%d")}
**Package Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📦 Package Contents

This package contains the complete NETRA Facial Recognition System, ready for deployment.

### Included:
- ✅ Complete source code (app/, tests/, scripts/)
- ✅ Configuration files (configs/)
- ✅ Docker deployment files
- ✅ Kubernetes manifests (k8s/)
- ✅ Monitoring setup (monitoring/)
- ✅ Comprehensive documentation (12+ guides)
- ✅ Installation scripts
- ✅ Test suite

### Not Included (will be created on installation):
- models/ (trained models - train your own or download separately)
- data/ (training data - add your own)
- logs/ (created at runtime)
- uploads/ (created at runtime)

## 🚀 Quick Start

### Step 1: Extract Package
```bash
unzip {zip_filename}
cd {project_name}
```

### Step 2: Install
```bash
# Create virtual environment
python -m venv netra-env
source netra-env/bin/activate  # Linux/Mac
# netra-env\\Scripts\\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install as global package
pip install -e .
```

### Step 3: Start Server
```bash
netra-server
# or
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Step 4: Access API
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 📚 Documentation

See the following documentation files in the package:
- `README.md` - Main overview
- `README_ENTERPRISE.md` - Enterprise guide
- `QUICKSTART.md` - 5-minute guide
- `INSTALLATION_GUIDE.md` - Platform-specific installation
- `DEPLOYMENT.md` - Deployment instructions
- `API_EXAMPLES.md` - API usage examples
- `FILE_STRUCTURE_GUIDE.md` - File explanations
- `SETUP_AND_TROUBLESHOOTING.md` - Setup help
- `DEBUG_REPORT.md` - Debug analysis
- `PROJECT_SUMMARY.md` - Project overview
- `FINAL_CHECKLIST.md` - Readiness checklist

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Validate installation
python validate_installation.py

# Run with coverage
pytest --cov=app tests/
```

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up -d

# Access services
# API: http://localhost:8000
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
```

## ☸️ Kubernetes Deployment

```bash
# Deploy to cluster
kubectl apply -f k8s/

# Check status
kubectl get pods -l app=netra
```

## 📞 Support

- **Documentation**: See all `.md` files
- **Issues**: Check logs in `logs/` directory
- **API Docs**: http://localhost:8000/docs
- **Troubleshooting**: See `SETUP_AND_TROUBLESHOOTING.md`

---

**Package Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Total Files**: {files_added}
**Package Size**: Ready for distribution
"""

        # Add README to ZIP
        readme_arcname = Path(project_name) / "PACKAGE_README.md"
        zipf.writestr(str(readme_arcname), readme_content)

        print(f"\n✅ Package created successfully!")
        print(f"📦 Package: {zip_path}")
        print(f"📊 Files included: {files_added}")
        print(f"📏 Size: {zip_path.stat().st_size / 1024 / 1024:.2f} MB")

        print("
📋 Package contents:"        print("  ├── app/ (8 Python files)")
        print("  ├── configs/ (configuration files)")
        print("  ├── k8s/ (5 Kubernetes manifests)")
        print("  ├── monitoring/ (Prometheus & Grafana configs)")
        print("  ├── scripts/ (utility scripts)")
        print("  ├── tests/ (test suite)")
        print("  ├── *.md (12 documentation files)")
        print("  ├── Dockerfile & docker-compose.yml")
        print("  ├── Makefile (automation)")
        print("  └── PACKAGE_README.md (this file)")

        print("
🎯 To use the package:"        print(f"  1. Unzip: unzip {zip_filename}")
        print(f"  2. cd {project_name}")
        print("  3. pip install -r requirements.txt")
        print("  4. pip install -e .")
        print("  5. netra-server")

        return zip_path

if __name__ == "__main__":
    create_release_package()
