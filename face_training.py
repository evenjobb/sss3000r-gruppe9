import os
import cv2
import numpy as np

# Function to get the images and labels from the dataset
def get_images_and_labels(dataset_path):
    face_images = []
    labels = []
    label_id = 0
    label_map = {}  # Map label names to IDs
    
    # Iterate through each subdirectory (each person's images)
    for person_name in os.listdir(dataset_path):
        person_dir = os.path.join(dataset_path, person_name)
        
        # Check if the item in the directory is a directory
        if os.path.isdir(person_dir):
            label_map[label_id] = person_name
            
            # Iterate through each image in the subdirectory
            for image_file in os.listdir(person_dir):
                image_path = os.path.join(person_dir, image_file)
                
                # Read the image in grayscale
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                
                # If the image is loaded successfully
                if image is not None:
                    face_images.append(image)
                    labels.append(label_id)
                    
            label_id += 1
    
    return face_images, np.array(labels), label_map

# Path to the directory containing the dataset
dataset_path = 'dataset'

# Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Create LBPH face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Get images and corresponding labels from the dataset
faces, labels, label_map = get_images_and_labels(dataset_path)

# Train the face recognizer
recognizer.train(faces, labels)

# Save the trained model to a file
recognizer.save('trainer/trainer.yml')

# Print information about the training process
print(f'Training complete. {len(label_map)} unique faces trained.')

# Print label map
print('Label Map:')
for label_id, person_name in label_map.items():
    print(f'ID: {label_id}, Name: {person_name}')
