# app/plant_api.py

import os
import tensorflow as tf
import numpy as np
from PIL import Image

# === Step 1: Load the trained model ===
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "model", "plant_classifier.keras")
model = tf.keras.models.load_model(model_path)
print("✅ Model loaded successfully.")

# === Step 2: Define class names (same order as during training) ===
class_names = ['Edible', 'Flower', 'Grass', 'Succulent', 'Tree']

# === Step 3: Define the prediction function ===
def classify_plant_image(image_file):
    """
    Classify an uploaded plant image into one of the predefined categories.
    
    Parameters:
        image_file (UploadedFile): The image file uploaded via Streamlit.
    Returns:
        str: Predicted class label (e.g. 'Flower', 'Tree', etc.).
    """
    # Reset file pointer and open the image
    image_file.seek(0)
    img = Image.open(image_file)
    # Convert to RGB (in case image is RGBA or grayscale)
    img = img.convert("RGB")
    # Resize to match the model's expected input size
    img = img.resize((224, 224))
    # Convert image to numpy array and normalize pixel values
    img_array = np.array(img) / 255.0
    # Expand dimensions to simulate a batch of size 1
    img_array = np.expand_dims(img_array, axis=0)
    # Perform prediction
    preds = model.predict(img_array)
    predicted_index = np.argmax(preds[0])
    predicted_label = class_names[predicted_index]
    return predicted_label