# NETRA : Facial Recognition system

A Deep Learning Facial recognition system using a Siamese Neural Network in supervised learning to verify identities by learning facial feature embeddings, ideal for secure authentication and identity verification applications.
siamese-project/
├─ app/                        # Core application
│  ├─ __init__.py
│  ├─ main.py                  # FastAPI app (inference + health + metrics)
│  ├─ model.py                 # Siamese PyTorch model & loader
│  ├─ dataset.py               # Folder-based dataset for training
│  ├─ preprocess.py            # OpenCV preprocessing utilities
│  ├─ train.py                 # Training loop with contrastive loss
│  ├─ utils.py                 # Logging, config, helper utilities
│  └─ inference_client.py      # Example Python client
│
├─ configs/
│  └─ config.yaml              # App + model config
│
├─ scripts/
│  ├─ entrypoint.sh            # Container startup script
│  └─ evaluate.py              # Evaluate trained model
│
├─ models/                     # Saved models (gitignored)
│  └─ siamese.pth
│
├─ tests/                      # Unit tests
│  ├─ test_app.py              # API tests (health, metrics, similarity)
│  └─ test_model.py            # Model forward test
│
├─ docker/
│  ├─ Dockerfile               # CPU multi-stage build
│  └─ Dockerfile.gpu           # GPU (CUDA 11.8 base)
│
├─ k8s/                        # Kubernetes manifests
│  ├─ deployment.yaml
│  ├─ service.yaml
│  └─ hpa.yaml
│
├─ helm/                       # Helm chart
│  ├─ Chart.yaml
│  ├─ values.yaml
│  └─ templates/
│     ├─ deployment.yaml
│     ├─ service.yaml
│     └─ _helpers.tpl
│
├─ monitoring/                 # Monitoring stack
│  └─ prometheus.yml
│
├─ torchscript/                # Model conversion/quantization
│  ├─ convert_to_torchscript.py
│  └─ quantize_example.py
│
├─ .github/workflows/          # CI/CD pipelines
│  ├─ ci.yml                   # Lint + Test
│  └─ docker-ci.yml            # Build & push Docker image
│
├─ .dockerignore
├─ .pre-commit-config.yaml
├─ docker-compose.yml
├─ docker-compose.monitor.yml  # App + Prometheus + Grafana
├─ requirements.txt
├─ requirements-dev.txt
├─ ARCHITECTURE.md
└─ README.md


