"""
Dataset and Data Loading utilities for Siamese Network training
"""

import os
import random
from pathlib import Path
from typing import Tuple, List
from PIL import Image
import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms


class SiameseDataset(Dataset):
    """
    Dataset class for Siamese Network training
    Creates pairs of images with labels (1 for same person, 0 for different)
    """
    
    def __init__(self, root_dir: str, transform=None):
        """
        Args:
            root_dir: Root directory with subdirectories for each person
            transform: Optional transform to be applied on images
        """
        self.root_dir = Path(root_dir)
        self.transform = transform
        
        # Build dataset structure
        self.classes = []
        self.class_to_images = {}
        
        for person_dir in self.root_dir.iterdir():
            if person_dir.is_dir():
                person_name = person_dir.name
                images = list(person_dir.glob('*.jpg')) + \
                        list(person_dir.glob('*.jpeg')) + \
                        list(person_dir.glob('*.png'))
                
                if len(images) > 0:
                    self.classes.append(person_name)
                    self.class_to_images[person_name] = images
        
        if len(self.classes) == 0:
            raise ValueError(f"No valid image classes found in {root_dir}")
        
        print(f"Loaded {len(self.classes)} classes with total images")
    
    def __len__(self) -> int:
        """Return the total number of possible pairs"""
        return len(self.classes) * 100  # Generate 100 pairs per class
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Generate a pair of images
        
        Returns:
            img1: First image tensor
            img2: Second image tensor
            label: 1 if same person, 0 if different
        """
        # Randomly decide if we want a positive or negative pair
        should_get_same_class = random.randint(0, 1)
        
        # Select first class and image
        class1 = random.choice(self.classes)
        img1_path = random.choice(self.class_to_images[class1])
        
        if should_get_same_class:
            # Positive pair - same person
            if len(self.class_to_images[class1]) < 2:
                # If only one image, use it twice
                img2_path = img1_path
            else:
                # Select different image of same person
                img2_path = random.choice(self.class_to_images[class1])
                while img2_path == img1_path and len(self.class_to_images[class1]) > 1:
                    img2_path = random.choice(self.class_to_images[class1])
            label = 1.0
        else:
            # Negative pair - different person
            class2 = random.choice(self.classes)
            while class2 == class1 and len(self.classes) > 1:
                class2 = random.choice(self.classes)
            img2_path = random.choice(self.class_to_images[class2])
            label = 0.0
        
        # Load images
        img1 = Image.open(img1_path).convert('RGB')
        img2 = Image.open(img2_path).convert('RGB')
        
        # Apply transforms
        if self.transform:
            img1 = self.transform(img1)
            img2 = self.transform(img2)
        
        return img1, img2, torch.tensor(label, dtype=torch.float32)


def get_transforms(image_size: int = 160, augment: bool = True):
    """
    Get image transformation pipeline
    
    Args:
        image_size: Target image size
        augment: Whether to apply data augmentation
        
    Returns:
        torchvision transforms composition
    """
    if augment:
        transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    else:
        transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    return transform


def create_dataloaders(train_dir: str, val_dir: str, batch_size: int = 32, 
                       image_size: int = 160, num_workers: int = 4):
    """
    Create training and validation dataloaders
    
    Args:
        train_dir: Training data directory
        val_dir: Validation data directory
        batch_size: Batch size for training
        image_size: Image size
        num_workers: Number of worker processes
        
    Returns:
        train_loader, val_loader
    """
    train_transform = get_transforms(image_size, augment=True)
    val_transform = get_transforms(image_size, augment=False)
    
    train_dataset = SiameseDataset(train_dir, transform=train_transform)
    val_dataset = SiameseDataset(val_dir, transform=val_transform)
    
    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    
    val_loader = torch.utils.data.DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    return train_loader, val_loader
