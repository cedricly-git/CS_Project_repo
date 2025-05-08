# app/predict_2.py

import os
import numpy as np
import tensorflow as tf
from PIL import Image


model_path = "/Users/graceyan/Downloads/St.Gallen /STUFF/plant_classifier3.keras"

# Load the model once at import time
_model = tf.keras.models.load_model(model_path)

# === Step 2: Define class names in the same order as training folders ===
_CLASS_NAMES = ["Edible", "Flower", "Grass", "Succulent", "Tree"]

# === Step 3: The prediction function ===
def classify_plant_image(image_file) -> str:
    """
    Accepts a Streamlit UploadedFile, preprocesses it,
    runs inference, and returns one of the five class labels.
    """
    # 1) Reset file pointer & open with PIL
    image_file.seek(0)
    img = Image.open(image_file)

    # 2) Convert to RGB & resize to model's input size
    img = img.convert("RGB").resize((224, 224))

    # 3) Turn into array, normalize to [0,1], add batch dim
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)  # shape (1,224,224,3)

    # 4) Run inference
    preds = _model.predict(arr)
    idx = int(np.argmax(preds[0]))

    # 5) Map to human-readable label
    return _CLASS_NAMES[idx]
