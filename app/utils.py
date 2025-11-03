"""
Utility functions for NETRA system
"""

import os
import pickle
import yaml
import torch
from pathlib import Path
from typing import Dict, Any, Optional


def load_config(config_path: str = "configs/config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    if not os.path.exists(config_path):
        print(f"⚠️  Config file not found at {config_path}, using defaults")
        return get_default_config()
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"⚠️  Error loading config: {e}, using defaults")
        return get_default_config()


def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration
    
    Returns:
        Default configuration dictionary
    """
    return {
        'app': {
            'host': '0.0.0.0',
            'port': 8000,
            'workers': 4,
            'reload': True
        },
        'model': {
            'path': 'models/siamese.pth',
            'embedding_dim': 128,
            'backbone': 'resnet50',
            'device': 'auto'
        },
        'training': {
            'epochs': 100,
            'batch_size': 32,
            'learning_rate': 0.001,
            'margin': 1.0,
            'weight_decay': 0.0001
        },
        'data': {
            'train_dir': 'data/train',
            'val_dir': 'data/val',
            'image_size': 160,
            'num_workers': 4
        }
    }


def get_device(device_preference: str = 'auto') -> torch.device:
    """
    Get the appropriate device for PyTorch
    
    Args:
        device_preference: 'auto', 'cpu', 'cuda', or 'mps'
        
    Returns:
        torch.device object
    """
    if device_preference == 'auto':
        if torch.cuda.is_available():
            return torch.device('cuda')
        elif torch.backends.mps.is_available():
            return torch.device('mps')
        else:
            return torch.device('cpu')
    else:
        return torch.device(device_preference)


def save_model(model: torch.nn.Module, path: str, metadata: Optional[Dict] = None):
    """
    Save model checkpoint
    
    Args:
        model: PyTorch model
        path: Save path
        metadata: Optional metadata to save with model
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    checkpoint = {
        'model_state_dict': model.state_dict(),
        'metadata': metadata or {}
    }
    
    torch.save(checkpoint, path)
    print(f"✅ Model saved to {path}")


def load_model(model: torch.nn.Module, path: str, device: torch.device):
    """
    Load model checkpoint
    
    Args:
        model: PyTorch model instance
        path: Path to checkpoint
        device: Device to load model on
        
    Returns:
        Loaded model and metadata
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found: {path}")
    
    checkpoint = torch.load(path, map_location=device)
    
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
        metadata = checkpoint.get('metadata', {})
    else:
        # Legacy format - just state dict
        model.load_state_dict(checkpoint)
        metadata = {}
    
    model.to(device)
    model.eval()
    
    return model, metadata


def create_directory_structure():
    """Create necessary directories for the project"""
    directories = [
        'models',
        'data/train',
        'data/val',
        'logs',
        'uploads',
        'configs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")


def count_parameters(model: torch.nn.Module) -> int:
    """
    Count the number of trainable parameters in a model
    
    Args:
        model: PyTorch model
        
    Returns:
        Number of trainable parameters
    """
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def format_time(seconds: float) -> str:
    """
    Format seconds into human-readable time
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


class AverageMeter:
    """Computes and stores the average and current value"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0
    
    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def calculate_accuracy(distances, labels, threshold=0.5):
    """
    Calculate accuracy for face verification
    
    Args:
        distances: Euclidean distances between embeddings
        labels: Ground truth labels (1 for same, 0 for different)
        threshold: Distance threshold for classification
        
    Returns:
        Accuracy score
    """
    predictions = (distances < threshold).float()
    correct = (predictions == labels).sum().item()
    total = labels.size(0)
    
    return correct / total


def find_optimal_threshold(distances, labels, num_thresholds=100):
    """
    Find optimal threshold for face verification
    
    Args:
        distances: Euclidean distances
        labels: Ground truth labels
        num_thresholds: Number of thresholds to test
        
    Returns:
        Optimal threshold and corresponding accuracy
    """
    min_dist = distances.min().item()
    max_dist = distances.max().item()
    
    thresholds = torch.linspace(min_dist, max_dist, num_thresholds)
    best_threshold = 0
    best_accuracy = 0
    
    for threshold in thresholds:
        accuracy = calculate_accuracy(distances, labels, threshold)
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_threshold = threshold.item()
    
    return best_threshold, best_accuracy
