"""
Siamese Neural Network Model for Face Recognition
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
from typing import Tuple


class SiameseNetwork(nn.Module):
    """
    Siamese Neural Network with shared weights for face verification
    """
    
    def __init__(self, embedding_dim: int = 128, backbone: str = "resnet50"):
        super(SiameseNetwork, self).__init__()
        
        self.embedding_dim = embedding_dim
        
        # Load pre-trained backbone
        if backbone == "resnet50":
            self.backbone = models.resnet50(pretrained=True)
            # Remove the final classification layer
            self.backbone = nn.Sequential(*list(self.backbone.children())[:-1])
            backbone_output_dim = 2048
        elif backbone == "resnet18":
            self.backbone = models.resnet18(pretrained=True)
            self.backbone = nn.Sequential(*list(self.backbone.children())[:-1])
            backbone_output_dim = 512
        else:
            raise ValueError(f"Unsupported backbone: {backbone}")
        
        # Embedding layer
        self.embedding = nn.Sequential(
            nn.Linear(backbone_output_dim, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, embedding_dim)
        )
        
    def forward_once(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for a single image
        
        Args:
            x: Input tensor of shape (batch_size, 3, H, W)
            
        Returns:
            Embedding tensor of shape (batch_size, embedding_dim)
        """
        # Extract features using backbone
        features = self.backbone(x)
        features = features.view(features.size(0), -1)
        
        # Generate embedding
        embedding = self.embedding(features)
        
        # L2 normalize the embedding
        embedding = F.normalize(embedding, p=2, dim=1)
        
        return embedding
    
    def forward(self, input1: torch.Tensor, input2: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass for a pair of images
        
        Args:
            input1: First image tensor
            input2: Second image tensor
            
        Returns:
            Tuple of embeddings (output1, output2)
        """
        output1 = self.forward_once(input1)
        output2 = self.forward_once(input2)
        
        return output1, output2


class ContrastiveLoss(nn.Module):
    """
    Contrastive loss function for Siamese Networks
    """
    
    def __init__(self, margin: float = 1.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin
    
    def forward(self, output1: torch.Tensor, output2: torch.Tensor, label: torch.Tensor) -> torch.Tensor:
        """
        Calculate contrastive loss
        
        Args:
            output1: First embedding
            output2: Second embedding
            label: 1 if same person, 0 if different
            
        Returns:
            Loss value
        """
        euclidean_distance = F.pairwise_distance(output1, output2)
        
        loss_contrastive = torch.mean(
            (label) * torch.pow(euclidean_distance, 2) +
            (1 - label) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2)
        )
        
        return loss_contrastive


def cosine_similarity(embedding1: torch.Tensor, embedding2: torch.Tensor) -> float:
    """
    Calculate cosine similarity between two embeddings
    
    Args:
        embedding1: First embedding
        embedding2: Second embedding
        
    Returns:
        Similarity score between 0 and 1
    """
    similarity = F.cosine_similarity(embedding1, embedding2, dim=1)
    return similarity.item()


def euclidean_distance(embedding1: torch.Tensor, embedding2: torch.Tensor) -> float:
    """
    Calculate Euclidean distance between two embeddings
    
    Args:
        embedding1: First embedding
        embedding2: Second embedding
        
    Returns:
        Distance value
    """
    distance = F.pairwise_distance(embedding1, embedding2)
    return distance.item()
