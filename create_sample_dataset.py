#!/usr/bin/env python3
"""
Simple Dataset Example for NETRA
Creates a sample dataset structure to demonstrate implementation
"""

import os
import shutil
from pathlib import Path

def create_sample_dataset():
    """Create a sample dataset structure for demonstration"""

    print("🎯 Creating Sample Dataset for NETRA")
    print("=" * 50)

    # Create sample dataset directory
    dataset_dir = "sample_faces"
    train_dir = Path(dataset_dir) / "train"
    val_dir = Path(dataset_dir) / "val"

    # Clean previous sample
    if Path(dataset_dir).exists():
        shutil.rmtree(dataset_dir)

    # Create directories
    train_dir.mkdir(parents=True)
    val_dir.mkdir(parents=True)

    # Create sample person directories
    people = ["alice", "bob", "charlie"]

    for person in people:
        (train_dir / person).mkdir()
        (val_dir / person).mkdir()

        print(f"👤 Created directories for: {person}")

    print("
✅ Sample dataset structure created!"    print(f"📁 Location: {dataset_dir}")
    print("
📋 Next steps:"    print("1. Add your face images to the person directories")
    print("2. Run: python dataset_setup.py --analyze sample_faces")
    print("3. Train: python app/train.py --config configs/config.yaml")

    print("
📖 See DATASET_IMPLEMENTATION_GUIDE.md for detailed instructions"
if __name__ == "__main__":
    create_sample_dataset()
