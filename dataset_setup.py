#!/usr/bin/env python3
"""
Dataset Setup Script for NETRA
Helps you organize and validate your face recognition dataset
"""

import os
import shutil
import random
from pathlib import Path
from PIL import Image
import argparse

def validate_image(image_path):
    """Validate if image is suitable for training"""
    try:
        with Image.open(image_path) as img:
            # Check size
            width, height = img.size
            if width < 160 or height < 160:
                return False, f"Image too small: {width}x{height} (minimum 160x160)"

            # Check format
            if img.format not in ['JPEG', 'PNG', 'JPG']:
                return False, f"Unsupported format: {img.format}"

            # Check if it's actually a face image (basic check)
            # You could add more sophisticated checks here

            return True, "Valid image"
    except Exception as e:
        return False, f"Error opening image: {e}"

def create_dataset_structure(source_dir, output_dir, train_ratio=0.8):
    """Create proper train/val split from source dataset"""

    source_path = Path(source_dir)
    output_path = Path(output_dir)

    if not source_path.exists():
        print(f"❌ Source directory {source_dir} does not exist!")
        return False

    # Create output directories
    train_dir = output_path / "train"
    val_dir = output_path / "val"

    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)

    total_images = 0
    valid_images = 0

    print(f"📁 Processing dataset from: {source_dir}")
    print(f"📁 Output directory: {output_dir}")
    print(f"📊 Train ratio: {train_ratio:.1%}\n")

    # Process each person directory
    for person_dir in source_path.iterdir():
        if not person_dir.is_dir():
            continue

        person_name = person_dir.name
        print(f"👤 Processing person: {person_name}")

        # Get all images for this person
        images = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            images.extend(list(person_dir.glob(ext)))

        if len(images) == 0:
            print(f"  ⚠️  No images found for {person_name}")
            continue

        # Validate images
        valid_images_list = []
        for img_path in images:
            is_valid, message = validate_image(img_path)
            if is_valid:
                valid_images_list.append(img_path)
                valid_images += 1
            else:
                print(f"  ❌ {img_path.name}: {message}")

        if len(valid_images_list) == 0:
            print(f"  ❌ No valid images for {person_name}")
            continue

        # Split into train/val
        random.shuffle(valid_images_list)
        split_point = int(len(valid_images_list) * train_ratio)

        train_images = valid_images_list[:split_point]
        val_images = valid_images_list[split_point:]

        # Create person directories
        person_train_dir = train_dir / person_name
        person_val_dir = val_dir / person_name

        person_train_dir.mkdir(exist_ok=True)
        person_val_dir.mkdir(exist_ok=True)

        # Copy images
        for i, img_path in enumerate(train_images):
            dest_path = person_train_dir / f"{person_name}_{i+1:03d}.jpg"
            shutil.copy2(img_path, dest_path)

        for i, img_path in enumerate(val_images):
            dest_path = person_val_dir / f"{person_name}_val_{i+1:03d}.jpg"
            shutil.copy2(img_path, dest_path)

        total_images += len(valid_images_list)
        print(f"  ✅ {len(train_images)} train, {len(val_images)} val images")

    print("\n📊 Summary:")
    print(f"  Total images processed: {total_images}")
    print(f"  Valid images: {valid_images}")
    print(f"  Train images: {sum(1 for _ in train_dir.rglob('*.jpg'))}")
    print(f"  Val images: {sum(1 for _ in val_dir.rglob('*.jpg'))}")

    return True

def analyze_dataset(dataset_dir):
    """Analyze existing dataset structure"""
    dataset_path = Path(dataset_dir)

    print(f"🔍 Analyzing dataset: {dataset_dir}\n")

    if not dataset_path.exists():
        print(f"❌ Dataset directory {dataset_dir} does not exist!")
        return False

    # Check structure
    train_dir = dataset_path / "train"
    val_dir = dataset_path / "val"

    if not (train_dir.exists() and val_dir.exists()):
        print("❌ Missing train/ or val/ directories")
        return False

    # Analyze each split
    for split_name, split_dir in [("Train", train_dir), ("Validation", val_dir)]:
        print(f"📊 {split_name} Set:")

        if not split_dir.exists():
            print(f"  ❌ {split_name.lower()} directory missing")
            continue

        person_dirs = [d for d in split_dir.iterdir() if d.is_dir()]
        total_images = 0

        if len(person_dirs) == 0:
            print(f"  ❌ No person directories found")
            continue

        print(f"  👥 People: {len(person_dirs)}")

        for person_dir in sorted(person_dirs):
            images = list(person_dir.glob("*.jpg")) + list(person_dir.glob("*.jpeg")) + list(person_dir.glob("*.png"))
            total_images += len(images)
            print(f"    {person_dir.name}: {len(images)} images")

        print(f"  📷 Total images: {total_images}")

        # Check for class balance
        image_counts = [len(list(person_dir.glob("*.jpg")) + list(person_dir.glob("*.jpeg")) + list(person_dir.glob("*.png")))
                       for person_dir in person_dirs]

        if len(set(image_counts)) > 1:
            print(f"  ⚠️  Class imbalance detected: {min(image_counts)}-{max(image_counts)} images per person")
        else:
            print(f"  ✅ Classes balanced: {image_counts[0]} images per person")

    return True

def main():
    parser = argparse.ArgumentParser(description="NETRA Dataset Setup Tool")
    parser.add_argument("--source", help="Source directory with raw images")
    parser.add_argument("--output", help="Output directory for organized dataset")
    parser.add_argument("--analyze", help="Analyze existing dataset")
    parser.add_argument("--train-ratio", type=float, default=0.8, help="Train/validation split ratio")

    args = parser.parse_args()

    if args.analyze:
        analyze_dataset(args.analyze)
    elif args.source and args.output:
        success = create_dataset_structure(args.source, args.output, args.train_ratio)
        if success:
            print("\n✅ Dataset setup complete!")
            print(f"📁 Your dataset is ready at: {args.output}")
            print("🚀 You can now train the model with:")
            print(f"   python app/train.py --config configs/config.yaml")
    else:
        parser.print_help()
        print("\n📖 Examples:")
        print("  # Analyze existing dataset")
        print("  python dataset_setup.py --analyze my-dataset")
        print("  ")
        print("  # Create new dataset structure")
        print("  python dataset_setup.py --source raw-images --output my-dataset")
        print("  ")
        print("  # Custom split ratio")
        print("  python dataset_setup.py --source raw-images --output my-dataset --train-ratio 0.7")

if __name__ == "__main__":
    main()
