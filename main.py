import requests
import cv2
import os

def download_image(url, save_path):
    """Downloads an image from the given URL and saves it to the specified path."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        print(f"Error downloading image: {response.status_code}")
        raise Exception(f"Error downloading image: {response.status_code}")

def detect_faces(image_path):
    """Detects faces in the given image path and returns the bounding box coordinates."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) > 0:
        return faces  # Return bounding box coordinates of all detected faces
    else:
        print("No faces detected in the image")
        return None

def extract_faces(image_path, bboxes, padding=10):
    """Extracts the face regions from the image based on the provided bounding boxes, with optional padding."""
    faces = []
    if bboxes is not None:
        image = cv2.imread(image_path)
        height, width, _ = image.shape
        for (x, y, w, h) in bboxes:
            # Calculate padding
            x1 = max(x - padding, 0)
            y1 = max(y - padding, 0)
            x2 = min(x + w + padding, width)
            y2 = min(y + h + padding, height)
            face = image[y1:y2, x1:x2]
            faces.append(face)
        return faces
    else:
        print("No bounding boxes provided or faces not detected")
        return None

def download_and_extract_faces(image_url, save_dir, padding=10):
    """Downloads an image from the URL, detects faces, and saves the extracted faces to the specified directory with padding."""
    download_image(image_url, "temp_image.jpg")  # Download to temporary file
    bboxes = detect_faces("temp_image.jpg")
    faces = extract_faces("temp_image.jpg", bboxes, padding)
    if faces is not None:
        for i, face in enumerate(faces):
            cv2.imwrite(os.path.join(save_dir, f"face_{i+1}.jpg"), face)  # Save each extracted face
    else:
        print("Failed to extract faces")
        raise Exception("Failed to extract faces")
    # Clean up the temporary file
    os.remove("temp_image.jpg")
