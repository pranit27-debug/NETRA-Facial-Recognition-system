#!/usr/bin/env python3
"""
Custom Dataset Training Example for NETRA
Shows how to train with your own face recognition dataset
"""

import os
import yaml
from pathlib import Path

def train_with_custom_dataset():
    """Example of training with custom dataset"""

    print("🎓 NETRA Custom Dataset Training Example")
    print("=" * 50)

    # Example dataset path (change this to your dataset)
    dataset_path = "my_faces"  # Your dataset directory

    # Check if dataset exists
    if not Path(dataset_path).exists():
        print(f"❌ Dataset not found at: {dataset_path}")
        print("\n📋 To create your dataset:")
        print("1. Organize images by person: person_name/image.jpg")
        print("2. Split into train/ and val/ directories")
        print("3. Run: python dataset_setup.py --analyze my-dataset")
        return

    # Load current config
    with open('configs/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Update dataset paths
    config['data']['train_dir'] = f"{dataset_path}/train"
    config['data']['val_dir'] = f"{dataset_path}/val"

    # Save updated config
    with open('configs/config_custom.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

     print("✅ Configuration updated for custom dataset")
     print(f"📁 Train directory: {config['data']['train_dir']}")
     print(f"📁 Val directory: {config['data']['val_dir']}")

 # Training parameters
    print("\n🎯 Recommended Training Parameters:")
    print(f"  Epochs: {config['training']['epochs']}")
    print(f"  Batch size: {config['training']['batch_size']}")
    print(f"  Learning rate: {config['training']['learning_rate']}")

    print("\n🚀 Training Commands:")
    print("  # Start training")
    print("  python app/train.py --config configs/config_custom.yaml\n")
    print("  # Train with custom parameters")
    print("  python app/train.py \\")
    print("    --config configs/config_custom.yaml \\")
    print("    --epochs 150 \\")
    print("    --batch_size 64 \\")
    print("    --learning_rate 0.0005")

    print("\n📊 Expected Results:")
    print("  - Training accuracy: 85-95% (depending on dataset quality)")
    print("  - Validation accuracy: 80-90%")
    print("  - Best model saved to: models/siamese_best_acc.pth")


def show_dataset_requirements():
    """Show dataset requirements and examples"""

    print("
📋 Dataset Requirements:"    print("  ✅ Minimum 2 people")
    print("  ✅ 5+ images per person (recommended: 10-20)")
    print("  ✅ 160x160+ pixel images")
    print("  ✅ JPG/PNG format")
    print("  ✅ Clear face photos")
    print("  ✅ Good lighting")

    print("
📁 Expected Structure:"    print("  my-dataset/")
    print("  ├── train/          # 80% of images")
    print("  │   ├── alice/")
    print("  │   │   ├── alice_001.jpg")
    print("  │   │   └── alice_002.jpg")
    print("  │   └── bob/")
    print("  │       └── bob_001.jpg")
    print("  └── val/           # 20% of images")
    print("      ├── alice/")
    print("      └── bob/")

if __name__ == "__main__":
    print("🎓 NETRA Custom Dataset Training Guide")
    print("=" * 60)

    # Show requirements
    show_dataset_requirements()

    # Check for existing dataset
    if Path("my_faces").exists():
        train_with_custom_dataset()
    else:
        print("
📝 Next Steps:"        print("1. Create your dataset (see DATASET_IMPLEMENTATION_GUIDE.md)")
        print("2. Organize images by person in train/ and val/ directories")
        print("3. Run: python dataset_setup.py --analyze my-dataset")
        print("4. Train: python app/train.py --config configs/config.yaml")

        print("
📖 For detailed instructions:"        print("  See: DATASET_IMPLEMENTATION_GUIDE.md")
        print("  Run: python dataset_setup.py --help")
