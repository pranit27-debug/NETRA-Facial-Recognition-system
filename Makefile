.PHONY: help install test lint format clean docker-build docker-run deploy

help:
	@echo "NETRA Facial Recognition System - Makefile Commands"
	@echo "===================================================="
	@echo "install          - Install dependencies"
	@echo "install-dev      - Install development dependencies"
	@echo "test             - Run tests"
	@echo "test-cov         - Run tests with coverage"
	@echo "lint             - Run linters"
	@echo "format           - Format code"
	@echo "clean            - Clean build artifacts"
	@echo "docker-build     - Build Docker image"
	@echo "docker-run       - Run with Docker Compose"
	@echo "docker-down      - Stop Docker containers"
	@echo "docker-logs      - View Docker logs"
	@echo "k8s-deploy       - Deploy to Kubernetes"
	@echo "k8s-delete       - Delete from Kubernetes"
	@echo "k8s-status       - Check Kubernetes status"
	@echo "train            - Train the model"
	@echo "train-custom     - Train with custom dataset"
	@echo "evaluate         - Evaluate the model"
	@echo "dataset-setup    - Setup custom dataset"
	@echo "dataset-analyze  - Analyze existing dataset"
	@echo "run-local        - Run development server"
	@echo "run-prod         - Run production server"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

test-cov:
	pytest --cov=app tests/ --cov-report=html

lint:
	flake8 app/ tests/
	mypy app/

format:
	black app/ tests/
	isort app/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf .coverage htmlcov/
	rm -rf build/ dist/ *.egg-info

docker-build:
	docker build -t netra-facial-recognition:latest .

docker-run:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

k8s-deploy:
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml
	kubectl apply -f k8s/ingress.yaml
	kubectl apply -f k8s/hpa.yaml

k8s-delete:
	kubectl delete -f k8s/

k8s-status:
	kubectl get pods -l app=netra
	kubectl get svc netra-service

train:
	python app/train.py --config configs/config.yaml

train-custom:
	python train_custom_dataset.py

evaluate:
	python scripts/evaluate.py --config configs/config.yaml

dataset-setup:
	python dataset_setup.py --help

dataset-analyze:
	@echo "Usage: python dataset_setup.py --analyze path/to/your/dataset"

run-local:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-prod:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
