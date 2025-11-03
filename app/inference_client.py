"""
Example client for NETRA API
"""

import requests
import argparse
from pathlib import Path


class NetraClient:
    """Client for interacting with NETRA API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def health_check(self):
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def detect_faces(self, image_path: str):
        """Detect faces in an image"""
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(f"{self.base_url}/api/v1/detect", files=files)
        
        return response.json()
    
    def verify_faces(self, image1_path: str, image2_path: str, threshold: float = 0.7):
        """Verify if two faces belong to the same person"""
        with open(image1_path, 'rb') as f1, open(image2_path, 'rb') as f2:
            files = {
                'image1': f1,
                'image2': f2
            }
            data = {'threshold': threshold}
            response = requests.post(
                f"{self.base_url}/api/v1/verify",
                files=files,
                data=data
            )
        
        return response.json()
    
    def calculate_similarity(self, image1_path: str, image2_path: str):
        """Calculate similarity between two faces"""
        with open(image1_path, 'rb') as f1, open(image2_path, 'rb') as f2:
            files = {
                'image1': f1,
                'image2': f2
            }
            response = requests.post(
                f"{self.base_url}/api/v1/similarity",
                files=files
            )
        
        return response.json()


def main():
    parser = argparse.ArgumentParser(description='NETRA API Client')
    parser.add_argument('--url', type=str, default='http://localhost:8000',
                        help='API base URL')
    parser.add_argument('--action', type=str, required=True,
                        choices=['health', 'detect', 'verify', 'similarity'],
                        help='Action to perform')
    parser.add_argument('--image1', type=str, help='Path to first image')
    parser.add_argument('--image2', type=str, help='Path to second image')
    parser.add_argument('--threshold', type=float, default=0.7,
                        help='Verification threshold')
    
    args = parser.parse_args()
    
    client = NetraClient(base_url=args.url)
    
    try:
        if args.action == 'health':
            result = client.health_check()
            print("Health Check:")
            print(f"  Status: {result['status']}")
            print(f"  Model Loaded: {result['model_loaded']}")
            print(f"  Device: {result['device']}")
        
        elif args.action == 'detect':
            if not args.image1:
                print("Error: --image1 required for detect action")
                return
            
            result = client.detect_faces(args.image1)
            print(f"\nDetected {result['face_count']} face(s):")
            for face in result['faces']:
                print(f"  Face {face['id']}: confidence={face['confidence']:.3f}")
        
        elif args.action == 'verify':
            if not args.image1 or not args.image2:
                print("Error: --image1 and --image2 required for verify action")
                return
            
            result = client.verify_faces(args.image1, args.image2, args.threshold)
            print(f"\nVerification Result:")
            print(f"  Similarity Score: {result['similarity_score']:.4f}")
            print(f"  Match: {result['is_match']}")
            print(f"  Threshold: {result['threshold_used']}")
        
        elif args.action == 'similarity':
            if not args.image1 or not args.image2:
                print("Error: --image1 and --image2 required for similarity action")
                return
            
            result = client.calculate_similarity(args.image1, args.image2)
            print(f"\nSimilarity Metrics:")
            print(f"  Cosine Similarity: {result['cosine_similarity']:.4f}")
            print(f"  Euclidean Distance: {result['euclidean_distance']:.4f}")
            print(f"  Normalized Similarity: {result['normalized_similarity']:.4f}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to connect to API - {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
