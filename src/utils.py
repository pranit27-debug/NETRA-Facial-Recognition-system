import os
import cv2
import numpy as np
import face_recognition
from typing import List, Tuple, Optional

def load_known_faces(model_path: str = 'models/face_recognition_model.pkl') -> Optional[tuple]:
    """
    Load the trained face recognition model
    
    Args:
        model_path (str): Path to the trained model file
        
    Returns:
        tuple: (known_face_encodings, known_face_names) or None if model not found
    """
    if not os.path.exists(model_path):
        print(f"Model file {model_path} not found!")
        return None
    
    try:
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        return model_data['encodings'], model_data['names']
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def recognize_faces(image_path: str, model_path: str = 'models/face_recognition_model.pkl') -> List[dict]:
    """
    Recognize faces in an image using the trained model
    
    Args:
        image_path (str): Path to the image file
        model_path (str): Path to the trained model file
        
    Returns:
        List[dict]: List of detected faces with their names and locations
    """
    # Load the trained model
    model_data = load_known_faces(model_path)
    if model_data is None:
        return []
    
    known_face_encodings, known_face_names = model_data
    
    # Load the image
    image = face_recognition.load_image_file(image_path)
    
    # Find all face locations and encodings in the image
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    recognized_faces = []
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare face with known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        
        # Calculate face distances
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        
        recognized_faces.append({
            'name': name,
            'location': {
                'top': int(top),
                'right': int(right),
                'bottom': int(bottom),
                'left': int(left)
            },
            'confidence': float(1 - face_distances[best_match_index])
        })
    
    return recognized_faces

def draw_face_boxes(image_path: str, output_path: str, recognized_faces: List[dict]) -> None:
    """
    Draw bounding boxes around recognized faces
    
    Args:
        image_path (str): Path to the input image
        output_path (str): Path to save the output image
        recognized_faces (List[dict]): List of recognized faces from recognize_faces()
    """
    # Read the image
    image = cv2.imread(image_path)
    
    # Draw rectangles and names
    for face in recognized_faces:
        top = face['location']['top']
        right = face['location']['right']
        bottom = face['location']['bottom']
        left = face['location']['left']
        name = face['name']
        confidence = face['confidence']
        
        # Draw rectangle
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        
        # Draw label background
        cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        
        # Draw label text
        label = f"{name} ({confidence:.2f})"
        cv2.putText(image, label, (left + 6, bottom - 6), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1)
    
    # Save the output image
    cv2.imwrite(output_path, image)
