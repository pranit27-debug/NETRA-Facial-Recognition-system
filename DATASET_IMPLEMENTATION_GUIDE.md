# NETRA Dataset Implementation Guide

Complete guide for implementing your own dataset in NETRA Facial Recognition System.

---

## 📊 Dataset Requirements

### **Minimum Dataset Requirements**
- **Classes**: At least 2 different people
- **Images per person**: Minimum 5 images (recommended: 10-20)
- **Image format**: JPG, JPEG, or PNG
- **Image size**: Minimum 160x160 pixels (recommended: 224x224+)
- **Total images**: Minimum 50+ for good training

### **Dataset Structure**

```
your-dataset/
├── train/                          # Training data (80% of total)
│   ├── person_001/
│   │   ├── image_001.jpg
│   │   ├── image_002.jpg
│   │   └── ...
│   ├── person_002/
│   │   ├── image_001.jpg
│   │   └── ...
│   └── person_003/
│       └── ...
└── val/                           # Validation data (20% of total)
    ├── person_001/
    │   ├── image_001.jpg
    │   └── ...
    └── person_002/
        └── ...
```

### **Image Quality Guidelines**
- ✅ **Clear faces** - No blurry or pixelated images
- ✅ **Good lighting** - Well-lit, no harsh shadows
- ✅ **Frontal/side views** - Include various angles
- ✅ **Different expressions** - Smiling, neutral, etc.
- ✅ **Clean background** - Avoid cluttered backgrounds
- ❌ **No sunglasses** - Eyes should be visible
- ❌ **No heavy makeup** - Natural appearance preferred
- ❌ **No extreme angles** - Avoid profile shots

---

## 🛠️ Step 1: Prepare Your Dataset

### **Organize Your Images**

1. **Create directory structure**:
```bash
mkdir -p your-dataset/train your-dataset/val
```

2. **Organize by person**:
```bash
# Training data (80% of your images)
your-dataset/train/
├── alice/
│   ├── alice_001.jpg
│   ├── alice_002.jpg
│   └── ...
├── bob/
│   ├── bob_001.jpg
│   └── ...
└── charlie/
    └── ...

# Validation data (20% of your images)
your-dataset/val/
├── alice/
│   ├── alice_val_001.jpg
│   └── ...
└── bob/
    └── ...
```

3. **Split your data**:
   - **80%** → `train/` folder
   - **20%** → `val/` folder

### **Naming Convention**
```
person_name/
├── person_name_001.jpg    # Training image 1
├── person_name_002.jpg    # Training image 2
├── person_name_003.jpg    # Training image 3
├── person_name_val_001.jpg # Validation image 1
└── person_name_val_002.jpg # Validation image 2
```

---

## ⚙️ Step 2: Configure Dataset Paths

### **Update Configuration**

Edit `configs/config.yaml`:

```yaml
data:
  train_dir: "your-dataset/train"    # Path to your training data
  val_dir: "your-dataset/val"        # Path to your validation data
  image_size: 160                    # Input image size
  num_workers: 4                     # Data loading workers
  batch_size: 32                     # Training batch size

model:
  embedding_dim: 128                 # Embedding dimension
  backbone: "resnet50"               # Backbone network
  device: "auto"                     # Auto-detect GPU/CPU

training:
  epochs: 100                        # Number of training epochs
  learning_rate: 0.001               # Learning rate
  margin: 1.0                        # Contrastive loss margin
  save_frequency: 10                 # Save model every N epochs
```

---

## 🎓 Step 3: Train with Your Dataset

### **Start Training**

```bash
# Method 1: Using the training script
python app/train.py --config configs/config.yaml

# Method 2: Using Makefile
make train

# Method 3: Custom training parameters
python app/train.py \
    --config configs/config.yaml \
    --epochs 150 \
    --batch_size 64 \
    --learning_rate 0.0005
```

### **Training Process**
1. **Data Loading**: Loads your dataset from specified paths
2. **Preprocessing**: Detects faces, aligns, and normalizes images
3. **Training Loop**:
   - Generates positive pairs (same person)
   - Generates negative pairs (different people)
   - Updates model weights using contrastive loss
4. **Validation**: Evaluates on validation set each epoch
5. **Checkpointing**: Saves best model based on validation accuracy

### **Training Output**
```
Epoch [1/100], Loss: 0.8472, Accuracy: 0.5234
Epoch [10/100], Loss: 0.2341, Accuracy: 0.8923
Epoch [50/100], Loss: 0.0456, Accuracy: 0.9765
Epoch [100/100], Loss: 0.0123, Accuracy: 0.9891

✓ Training completed!
✓ Best model saved: models/siamese_best_acc.pth
✓ Final accuracy: 98.91%
```

---

## 🧪 Step 4: Test Your Model

### **Evaluate Performance**

```bash
# Run evaluation script
python scripts/evaluate.py --config configs/config.yaml

# Output includes:
# - Accuracy, Precision, Recall, F1-score
# - ROC curve analysis
# - Distance distribution plots
# - Optimal threshold calculation
```

### **Test API Endpoints**

1. **Start the server**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. **Test face detection**:
```bash
curl -X POST "http://localhost:8000/api/v1/detect" \
  -F "image=@your-dataset/train/alice/alice_001.jpg"
```

3. **Test face verification**:
```bash
curl -X POST "http://localhost:8000/api/v1/verify" \
  -F "image1=@your-dataset/train/alice/alice_001.jpg" \
  -F "image2=@your-dataset/val/alice/alice_val_001.jpg" \
  -F "threshold=0.7"
```

### **Expected API Response**
```json
{
  "status": "success",
  "similarity_score": 0.8943,
  "is_match": true,
  "threshold_used": 0.7
}
```

---

## 🔧 Step 5: Optimize Your Dataset

### **Dataset Quality Improvements**

1. **Increase variety**:
   - Different lighting conditions
   - Various facial expressions
   - Different head poses (frontal, ¾ view, side)
   - With/without glasses (if applicable)

2. **Balance classes**:
   - Ensure each person has similar number of images
   - Avoid class imbalance

3. **Image preprocessing**:
   - Crop to face region only
   - Ensure consistent image quality
   - Remove duplicates

### **Dataset Augmentation**

The system automatically applies:
- Random horizontal flips
- Color jittering
- Random cropping
- Normalization

### **Add More Data**

For better accuracy:
- **Small dataset** (50-200 images): 50-100 epochs
- **Medium dataset** (200-1000 images): 30-50 epochs
- **Large dataset** (1000+ images): 20-30 epochs

---

## 📊 Step 6: Monitor Training Progress

### **Training Metrics**

Monitor these metrics during training:
- **Loss**: Should decrease over time
- **Accuracy**: Should increase and plateau
- **Validation metrics**: Should follow training metrics

### **Early Stopping**

Training stops early if:
- Validation loss doesn't improve for 10+ epochs
- Model starts overfitting

### **Model Checkpoints**

Models are saved:
- Every N epochs (`save_frequency`)
- Best validation accuracy model
- Final model after training

---

## 🛠️ Step 7: Deploy with Your Dataset

### **Update Configuration for Production**

```yaml
# configs/config.yaml
model:
  path: "models/siamese_best_acc.pth"  # Your trained model
  device: "auto"                       # Use GPU if available

inference:
  default_threshold: 0.7               # Based on your validation
  batch_size: 1
  max_faces_per_image: 10
```

### **Package Your Model**

```bash
# Create deployment package
python create_release_package.py

# Include your trained model
cp models/siamese_best_acc.pth package/models/
```

---

## 📋 Complete Example Dataset

### **Sample Dataset Structure**

```
my_faces/
├── train/
│   ├── john_doe/
│   │   ├── john_001.jpg    # Frontal view, neutral
│   │   ├── john_002.jpg    # Slight smile
│   │   ├── john_003.jpg    # With glasses
│   │   ├── john_004.jpg    # Different lighting
│   │   └── john_005.jpg    # Side view
│   ├── jane_smith/
│   │   ├── jane_001.jpg
│   │   ├── jane_002.jpg
│   │   ├── jane_003.jpg
│   │   └── jane_004.jpg
│   └── bob_johnson/
│       ├── bob_001.jpg
│       ├── bob_002.jpg
│       └── bob_003.jpg
└── val/
    ├── john_doe/
    │   ├── john_val_001.jpg
    │   └── john_val_002.jpg
    └── jane_smith/
        └── jane_val_001.jpg
```

### **Expected Results**
- **Training images**: ~15 per person
- **Validation images**: ~3-5 per person
- **Total images**: ~50-100
- **Expected accuracy**: 85-95% with good data

---

## 🚨 Common Dataset Issues

### **Issue 1: Poor Image Quality**
**Problem**: Blurry, dark, or small images
**Solution**: Ensure minimum 160x160 pixels, good lighting

### **Issue 2: Class Imbalance**
**Problem**: Some people have 50 images, others have 5
**Solution**: Balance classes (10-20 images per person)

### **Issue 3: Similar Faces**
**Problem**: People look too similar, model confused
**Solution**: More diverse angles, expressions, lighting

### **Issue 4: Insufficient Data**
**Problem**: <50 total images
**Solution**: Collect more diverse images per person

---

## 📈 Advanced Dataset Techniques

### **1. Data Augmentation**
The system automatically applies:
- Horizontal flips
- Color adjustments
- Cropping variations
- Normalization

### **2. Cross-Validation**
Split your data into multiple train/val folds for robust evaluation.

### **3. Domain Adaptation**
If your deployment environment differs from training data:
- Include diverse lighting conditions
- Add different camera types
- Include various backgrounds

---

## 🎯 Best Practices Summary

### **Dataset Preparation**
1. **Organize by person** in separate folders
2. **Split 80/20** train/validation
3. **Balance classes** (similar images per person)
4. **Use good quality images** (160x160+, well-lit)
5. **Include variety** (angles, expressions, lighting)

### **Training**
1. **Start with defaults** in config
2. **Monitor metrics** during training
3. **Use validation set** for early stopping
4. **Save best model** based on validation accuracy

### **Evaluation**
1. **Test on unseen data** (validation set)
2. **Check ROC curves** for threshold selection
3. **Analyze confusion matrix** for error patterns
4. **Validate API endpoints** with your data

---

## 📞 Need Help?

If you encounter issues:
1. Check `SETUP_AND_TROUBLESHOOTING.md`
2. Validate your dataset structure matches the requirements
3. Check logs in `logs/` directory
4. Review training metrics and adjust parameters

---

**Ready to implement your dataset!** 🎯

Follow these steps to successfully train NETRA with your own face recognition data.
