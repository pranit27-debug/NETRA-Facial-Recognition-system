import os
import cv2
import face_recognition
import numpy as np
import pickle
from pathlib import Path

def train_model(dataset_path='dataset'):
    """
    Train the face recognition model on the dataset
    
    Args:
        dataset_path (str): Path to the dataset directory containing subdirectories for each person
    """
    known_face_encodings = []
    known_face_names = []
    
    # Ensure dataset directory exists
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset directory '{dataset_path}' not found!")
        return False
    
    # Loop through each person in the dataset
    for person_dir in Path(dataset_path).iterdir():
        if not person_dir.is_dir():
            continue
            
        person_name = person_dir.name
        print(f"Training on {person_name}...")
        
        # Process each image of the person
        for img_path in person_dir.glob('*.jpg') + person_dir.glob('*.jpeg') + person_dir.glob('*.png'):
            # Load the image
            image = face_recognition.load_image_file(img_path)
            
            # Get face encodings for the image
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) > 0:
                # Use the first face found in the image
                known_face_encodings.append(face_encodings[0])
                known_face_names.append(person_name)
    
    # Save the trained model
    if len(known_face_encodings) > 0:
        model_data = {
            'encodings': known_face_encodings,
            'names': known_face_names
        }
        
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Save the model
        with open('models/face_recognition_model.pkl', 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"\nTraining complete! Model saved with {len(known_face_encodings)} face encodings.")
        return True
    else:
        print("Error: No faces found in the dataset!")
        return False

if __name__ == "__main__":
    train_model()
