"""
Unit tests for Siamese Neural Network model
"""

import pytest
import torch
from app.model import SiameseNetwork, ContrastiveLoss, cosine_similarity, euclidean_distance


def test_siamese_network_initialization():
    """Test model initialization"""
    model = SiameseNetwork(embedding_dim=128, backbone="resnet50")
    assert model is not None
    assert model.embedding_dim == 128


def test_siamese_network_forward_once():
    """Test single forward pass"""
    model = SiameseNetwork(embedding_dim=128, backbone="resnet18")
    model.eval()
    
    # Create dummy input
    x = torch.randn(2, 3, 160, 160)
    
    with torch.no_grad():
        output = model.forward_once(x)
    
    assert output.shape == (2, 128)
    # Check L2 normalization
    norms = torch.norm(output, p=2, dim=1)
    assert torch.allclose(norms, torch.ones_like(norms), atol=1e-5)


def test_siamese_network_forward():
    """Test paired forward pass"""
    model = SiameseNetwork(embedding_dim=128, backbone="resnet18")
    model.eval()
    
    # Create dummy inputs
    x1 = torch.randn(2, 3, 160, 160)
    x2 = torch.randn(2, 3, 160, 160)
    
    with torch.no_grad():
        output1, output2 = model(x1, x2)
    
    assert output1.shape == (2, 128)
    assert output2.shape == (2, 128)


def test_contrastive_loss():
    """Test contrastive loss calculation"""
    criterion = ContrastiveLoss(margin=1.0)
    
    # Create dummy embeddings
    output1 = torch.randn(4, 128)
    output2 = torch.randn(4, 128)
    labels = torch.tensor([1.0, 0.0, 1.0, 0.0])
    
    loss = criterion(output1, output2, labels)
    
    assert loss.item() >= 0
    assert not torch.isnan(loss)


def test_cosine_similarity():
    """Test cosine similarity calculation"""
    embedding1 = torch.randn(1, 128)
    embedding2 = torch.randn(1, 128)
    
    similarity = cosine_similarity(embedding1, embedding2)
    
    assert isinstance(similarity, float)
    assert -1 <= similarity <= 1


def test_euclidean_distance():
    """Test Euclidean distance calculation"""
    embedding1 = torch.randn(1, 128)
    embedding2 = torch.randn(1, 128)
    
    distance = euclidean_distance(embedding1, embedding2)
    
    assert isinstance(distance, float)
    assert distance >= 0


def test_model_same_weights():
    """Test that backbone weights are shared"""
    model = SiameseNetwork(embedding_dim=128, backbone="resnet18")
    
    x1 = torch.randn(1, 3, 160, 160)
    x2 = x1.clone()
    
    model.eval()
    with torch.no_grad():
        output1, output2 = model(x1, x2)
    
    # Same input should produce same output
    assert torch.allclose(output1, output2, atol=1e-5)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
