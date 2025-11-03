# NETRA System Architecture

## Overview

NETRA is a facial recognition system built using modern Python technologies and computer vision libraries. The system is designed to be modular, scalable, and easy to deploy.

## System Components

### 1. Core Components

#### Face Detection Module
- **Technology**: face_recognition library (built on glib)
- **Purpose**: Detect faces in images and video streams
- **Key Features**:
  - Multi-face detection
  - Face location extraction
  - Real-time processing capability

#### Face Recognition Module
- **Technology**: face_recognition library with deep learning embeddings
- **Purpose**: Identify and verify faces against a trained model
- **Key Features**:
  - Face encoding generation (128-dimensional embeddings)
  - Face comparison using Euclidean distance
  - Confidence scoring

#### Training Module
- **Purpose**: Train the face recognition model on custom datasets
- **Process**:
  1. Load images from dataset directory
  2. Extract face encodings for each person
  3. Store encodings with associated names
  4. Save model as pickle file

### 2. API Layer

#### Flask REST API
- **Endpoints**:
  - `GET /`: Health check
  - `POST /detect`: Face detection
  - `POST /recognize`: Face recognition (future)
  - `POST /train`: Model training (future)

#### Request/Response Flow
```
Client Request → Flask Router → Handler Function → 
Face Detection/Recognition → Response Formatting → Client Response
```

### 3. Data Storage

#### Model Storage
- **Format**: Pickle (.pl) files
- **Contents**: Face encodings and associated names
- **Location**: `models/` directory

#### Dataset Structure
```
dataset/
├── person1/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── image3.jpg
└── person2/
    ├── image1.jpg
    └── image2.jpg
```

#### Temporary Storage
- **Upload Directory**: Stores temporarily uploaded images
- **Clean up**: Files are removed after processing

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Client Layer                         │
│  (Web Browser, Mobile App, API Client)                  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Flask API Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Routes     │  │  Middleware  │  │   Handlers   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│               Business Logic Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Detection  │  │ Recognition  │  │   Training   │ │
│  │    Module    │  │    Module    │  │    Module    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Core Libraries                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │face_recognition│ │   OpenCV    │  │    NumPy     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Data Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Models     │  │   Dataset    │  │   Uploads    │ │
│  │  (.pkl files)│  │  (images)    │  │  (temp)      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Model Architecture

### Face Recognition Pipeline

1. **Image Input**: Accept image from user
2. **Pre-processing**: 
   - Convert to RGB format
   - Resize if necessary
3. **Face Detection**:
   - Use HOG (Histogram of Oriented Gradients) or CNN
   - Extract face bounding boxes
4. **Face Encoding**:
   - Generate 128-dimensional face embeddings
   - Use pre-trained ResNet model
5. **Face Comparison**:
   - Calculate Euclidean distance between encodings
   - Apply threshold for matching
6. **Result Generation**:
   - Return matched identities with confidence scores

### Training Process

```
Dataset Images → Face Detection → Face Encoding → 
Model Storage → Serialization (Pickle)
```

## Deployment Architecture

### Docker Container(contanirazation)
```
┌─────────────────────────────────────┐
│         Docker Container             │
│  ┌───────────────────────────────┐  │
│  │      Python 3.9 Runtime       │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │   Flask Application     │  │  │
│  │  │   (Port 5000)           │  │  │
│  │  └─────────────────────────┘  │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │   Volume Mounts         │  │  │
│  │  │   - models/             │  │  │
│  │  │   - dataset/            │  │  │
│  │  │   - uploads/            │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

## Security Considerations

1. **Input Validation**: All uploaded files are validated
2. **File Type Restrictions**: Only image files are accepted
3. **Temporary Storage**: Uploaded files are deleted after processing
4. **Model Protection**: Models are stored securely
5. **API Rate Limiting**: (Future implementation)

## Performance Optimization

1. **Face Detection**: Use HOG for CPU, CNN for GPU
2. **Batch Processing**: Process multiple faces simultaneously
3. **Caching**: Cache frequently accessed models
4. **Async Processing**: Use async for long-running tasks (future)

## Scalability

### Horizontal Scaling
- Deploy multiple Flask instances behind a load balancer
- Use shared storage for models and datasets
- Implement Redis for session management

### Vertical Scaling
- Optimize face detection algorithms
- Use GPU acceleration for faster processing
- Implement model quantization

## Future Enhancements

1. **Real-time Video Processing**: Add webcam support
2. **Database Integration**: Store face encodings in database
3. **User Management**: Add authentication and authorization
4. **Advanced Analytics**: Track recognition statistics
5. **Mobile SDK**: Provide mobile app integration
6. **Cloud Deployment**: Deploy on AWS/Azure/GCP
