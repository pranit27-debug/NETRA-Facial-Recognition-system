"""
Model evaluation script
"""

import os
import argparse
import torch
import numpy as np
from sklearn.metrics import roc_curve, auc, confusion_matrix
import matplotlib.pyplot as plt
from pathlib import Path

from app.model import SiameseNetwork
from app.dataset import create_dataloaders
from app.utils import load_config, get_device, load_model


def evaluate_model(model, data_loader, device):
    """Evaluate model on dataset"""
    model.eval()
    
    all_distances = []
    all_labels = []
    
    with torch.no_grad():
        for img1, img2, labels in data_loader:
            img1, img2, labels = img1.to(device), img2.to(device), labels.to(device)
            
            # Get embeddings
            output1, output2 = model(img1, img2)
            
            # Calculate distances
            distances = torch.nn.functional.pairwise_distance(output1, output2)
            
            all_distances.extend(distances.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    return np.array(all_distances), np.array(all_labels)


def plot_roc_curve(distances, labels, save_path='logs/roc_curve.png'):
    """Plot ROC curve"""
    # Convert distances to similarity scores (inverse)
    similarities = 1 - (distances / distances.max())
    
    fpr, tpr, thresholds = roc_curve(labels, similarities)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(10, 8))
    plt.plot(fpr, tpr, color='darkorange', lw=2, 
             label=f'ROC curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ ROC curve saved to {save_path}")
    
    return roc_auc


def plot_distance_distribution(distances, labels, save_path='logs/distance_distribution.png'):
    """Plot distance distribution"""
    same_person = distances[labels == 1]
    different_person = distances[labels == 0]
    
    plt.figure(figsize=(12, 6))
    
    plt.hist(same_person, bins=50, alpha=0.6, label='Same Person', color='green')
    plt.hist(different_person, bins=50, alpha=0.6, label='Different Person', color='red')
    
    plt.xlabel('Euclidean Distance')
    plt.ylabel('Frequency')
    plt.title('Distance Distribution')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Distance distribution saved to {save_path}")


def find_best_threshold(distances, labels):
    """Find optimal threshold"""
    thresholds = np.linspace(distances.min(), distances.max(), 100)
    best_threshold = 0
    best_accuracy = 0
    
    for threshold in thresholds:
        predictions = (distances < threshold).astype(int)
        accuracy = (predictions == labels).mean()
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_threshold = threshold
    
    return best_threshold, best_accuracy


def calculate_metrics(distances, labels, threshold):
    """Calculate evaluation metrics"""
    predictions = (distances < threshold).astype(int)
    
    # Confusion matrix
    tn, fp, fn, tp = confusion_matrix(labels, predictions).ravel()
    
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'true_positives': tp,
        'true_negatives': tn,
        'false_positives': fp,
        'false_negatives': fn
    }


def main(args):
    """Main evaluation function"""
    
    # Load configuration
    config = load_config(args.config)
    
    # Set device
    device = get_device(config['model'].get('device', 'auto'))
    print(f"Using device: {device}")
    
    # Load model
    print("Loading model...")
    model = SiameseNetwork(
        embedding_dim=config['model']['embedding_dim'],
        backbone=config['model']['backbone']
    )
    model, metadata = load_model(model, config['model']['path'], device)
    print(f"✅ Model loaded from {config['model']['path']}")
    
    if metadata:
        print(f"Model metadata: {metadata}")
    
    # Load validation data
    print("Loading validation dataset...")
    _, val_loader = create_dataloaders(
        train_dir=config['data']['train_dir'],
        val_dir=config['data']['val_dir'],
        batch_size=config['training']['batch_size'],
        image_size=config['data']['image_size'],
        num_workers=config['data'].get('num_workers', 4)
    )
    
    # Evaluate model
    print("\nEvaluating model...")
    distances, labels = evaluate_model(model, val_loader, device)
    
    # Find optimal threshold
    optimal_threshold, best_accuracy = find_best_threshold(distances, labels)
    print(f"\n📊 Optimal threshold: {optimal_threshold:.4f}")
    print(f"📊 Best accuracy: {best_accuracy:.4f}")
    
    # Calculate metrics
    metrics = calculate_metrics(distances, labels, optimal_threshold)
    
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1 Score:  {metrics['f1_score']:.4f}")
    print(f"\nConfusion Matrix:")
    print(f"  True Positives:  {metrics['true_positives']}")
    print(f"  True Negatives:  {metrics['true_negatives']}")
    print(f"  False Positives: {metrics['false_positives']}")
    print(f"  False Negatives: {metrics['false_negatives']}")
    print("=" * 60)
    
    # Plot ROC curve
    roc_auc = plot_roc_curve(distances, labels)
    print(f"\n📈 ROC AUC: {roc_auc:.4f}")
    
    # Plot distance distribution
    plot_distance_distribution(distances, labels)
    
    print("\n✨ Evaluation complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate Siamese Network')
    parser.add_argument('--config', type=str, default='configs/config.yaml',
                        help='Path to config file')
    
    args = parser.parse_args()
    main(args)
