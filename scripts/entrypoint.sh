#!/bin/bash
set -e

echo "🚀 Starting NETRA Facial Recognition System..."

# Create necessary directories
mkdir -p /app/models
mkdir -p /app/logs
mkdir -p /app/uploads
mkdir -p /app/data/train
mkdir -p /app/data/val

# Check if model exists
if [ ! -f "/app/models/siamese.pth" ]; then
    echo "⚠️  No pre-trained model found. Starting with untrained model."
fi

# Start the application
echo "✨ Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
