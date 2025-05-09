# app/plant_api.py

import os
from io import BytesIO

import numpy as np
import tensorflow as tf
from PIL import Image

# — Step 1: locate & load your .keras model —
script_dir = os.path.dirname(os.path.abspath(__file__))
# model_dir sits alongside app/ and plant_images/, one level up
model_dir = os.path.join(script_dir, os.pardir, "model")
model_path = os.path.join(model_dir, "plant_classifier.keras")

# load once at import time
_model = tf.keras.models.load_model(model_path)

# — Step 2: class names in the same order as your training folders —
_CLASS_NAMES = ["Edible", "Flower", "Grass", "Succulent", "Tree"]

def classify_plant_image(image_bytes: bytes) -> str:
    """
    Accepts the raw bytes of an uploaded plant image,
    preprocesses it, runs inference, and returns
    one of the five class labels.
    """
    # 1) open from raw bytes
    buf = BytesIO(image_bytes)
    img = Image.open(buf)

    # 2) ensure RGB & resize
    img = img.convert("RGB").resize((224, 224))

    # 3) to numpy array, float32, leave in [0–255]
    arr = np.array(img).astype("float32")

    # 4) batch dimension
    batch = np.expand_dims(arr, axis=0)

    # 5) predict
    preds = _model.predict(batch)
    idx = int(np.argmax(preds[0]))
    return _CLASS_NAMES[idx]