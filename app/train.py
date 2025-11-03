"""
Training script for Siamese Neural Network
"""

import os
import argparse
import time
import torch
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter

from app.model import SiameseNetwork, ContrastiveLoss
from app.dataset import create_dataloaders
from app.utils import (
    load_config, get_device, save_model, 
    count_parameters, format_time, AverageMeter,
    calculate_accuracy, find_optimal_threshold
)


def train_epoch(model, train_loader, criterion, optimizer, device, epoch):
    """Train for one epoch"""
    model.train()
    
    losses = AverageMeter()
    accuracies = AverageMeter()
    
    start_time = time.time()
    
    for batch_idx, (img1, img2, labels) in enumerate(train_loader):
        img1, img2, labels = img1.to(device), img2.to(device), labels.to(device)
        
        # Forward pass
        output1, output2 = model(img1, img2)
        loss = criterion(output1, output2, labels)
        
        # Calculate accuracy
        distances = torch.nn.functional.pairwise_distance(output1, output2)
        accuracy = calculate_accuracy(distances, labels)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # Update metrics
        losses.update(loss.item(), img1.size(0))
        accuracies.update(accuracy, img1.size(0))
        
        if (batch_idx + 1) % 10 == 0:
            print(f'Epoch [{epoch}] Batch [{batch_idx + 1}/{len(train_loader)}] '
                  f'Loss: {losses.avg:.4f} Acc: {accuracies.avg:.4f}')
    
    epoch_time = time.time() - start_time
    
    return losses.avg, accuracies.avg, epoch_time


def validate(model, val_loader, criterion, device):
    """Validate the model"""
    model.eval()
    
    losses = AverageMeter()
    all_distances = []
    all_labels = []
    
    with torch.no_grad():
        for img1, img2, labels in val_loader:
            img1, img2, labels = img1.to(device), img2.to(device), labels.to(device)
            
            # Forward pass
            output1, output2 = model(img1, img2)
            loss = criterion(output1, output2, labels)
            
            # Calculate distances
            distances = torch.nn.functional.pairwise_distance(output1, output2)
            
            losses.update(loss.item(), img1.size(0))
            all_distances.append(distances)
            all_labels.append(labels)
    
    # Concatenate all distances and labels
    all_distances = torch.cat(all_distances)
    all_labels = torch.cat(all_labels)
    
    # Find optimal threshold
    optimal_threshold, best_accuracy = find_optimal_threshold(all_distances, all_labels)
    
    return losses.avg, best_accuracy, optimal_threshold


def main(args):
    """Main training function"""
    
    # Load configuration
    config = load_config(args.config)
    
    # Override config with command line arguments
    if args.epochs:
        config['training']['epochs'] = args.epochs
    if args.batch_size:
        config['training']['batch_size'] = args.batch_size
    if args.learning_rate:
        config['training']['learning_rate'] = args.learning_rate
    
    # Set device
    device = get_device(config['model'].get('device', 'auto'))
    print(f"Using device: {device}")
    
    # Create dataloaders
    print("Loading datasets...")
    train_loader, val_loader = create_dataloaders(
        train_dir=config['data']['train_dir'],
        val_dir=config['data']['val_dir'],
        batch_size=config['training']['batch_size'],
        image_size=config['data']['image_size'],
        num_workers=config['data'].get('num_workers', 4)
    )
    
    print(f"Train batches: {len(train_loader)}, Val batches: {len(val_loader)}")
    
    # Initialize model
    model = SiameseNetwork(
        embedding_dim=config['model']['embedding_dim'],
        backbone=config['model']['backbone']
    )
    model.to(device)
    
    print(f"Model parameters: {count_parameters(model):,}")
    
    # Loss and optimizer
    criterion = ContrastiveLoss(margin=config['training']['margin'])
    optimizer = optim.Adam(
        model.parameters(),
        lr=config['training']['learning_rate'],
        weight_decay=config['training'].get('weight_decay', 0.0001)
    )
    
    # Learning rate scheduler
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=5, verbose=True
    )
    
    # TensorBoard writer
    writer = SummaryWriter(log_dir='logs')
    
    # Training loop
    best_val_loss = float('inf')
    best_accuracy = 0
    
    print("\nStarting training...")
    print("=" * 80)
    
    for epoch in range(1, config['training']['epochs'] + 1):
        print(f"\nEpoch {epoch}/{config['training']['epochs']}")
        print("-" * 80)
        
        # Train
        train_loss, train_acc, epoch_time = train_epoch(
            model, train_loader, criterion, optimizer, device, epoch
        )
        
        # Validate
        val_loss, val_acc, optimal_threshold = validate(
            model, val_loader, criterion, device
        )
        
        # Update learning rate
        scheduler.step(val_loss)
        
        # Log metrics
        writer.add_scalar('Loss/train', train_loss, epoch)
        writer.add_scalar('Loss/val', val_loss, epoch)
        writer.add_scalar('Accuracy/train', train_acc, epoch)
        writer.add_scalar('Accuracy/val', val_acc, epoch)
        writer.add_scalar('Learning_Rate', optimizer.param_groups[0]['lr'], epoch)
        
        # Print epoch summary
        print(f"\nEpoch {epoch} Summary:")
        print(f"  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
        print(f"  Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
        print(f"  Optimal Threshold: {optimal_threshold:.4f}")
        print(f"  Time: {format_time(epoch_time)}")
        
        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            save_model(
                model,
                config['model']['path'],
                metadata={
                    'epoch': epoch,
                    'val_loss': val_loss,
                    'val_accuracy': val_acc,
                    'optimal_threshold': optimal_threshold
                }
            )
            print(f"  ✅ Best model saved!")
        
        if val_acc > best_accuracy:
            best_accuracy = val_acc
            save_model(
                model,
                config['model']['path'].replace('.pth', '_best_acc.pth'),
                metadata={
                    'epoch': epoch,
                    'val_loss': val_loss,
                    'val_accuracy': val_acc,
                    'optimal_threshold': optimal_threshold
                }
            )
    
    print("\n" + "=" * 80)
    print("Training completed!")
    print(f"Best validation loss: {best_val_loss:.4f}")
    print(f"Best validation accuracy: {best_accuracy:.4f}")
    
    writer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train Siamese Network')
    parser.add_argument('--config', type=str, default='configs/config.yaml',
                        help='Path to config file')
    parser.add_argument('--epochs', type=int, default=None,
                        help='Number of epochs')
    parser.add_argument('--batch-size', type=int, default=None,
                        help='Batch size')
    parser.add_argument('--learning-rate', type=float, default=None,
                        help='Learning rate')
    
    args = parser.parse_args()
    main(args)
