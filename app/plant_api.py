# --- Plant Classification & Recognition ---
# This script is the the feature of the plant classification web app.
# It load a pre-trained Keras model and provides a function to classify plant images.
# And returns the class label of the plant image.

# --- Reference ---
# https://www.tensorflow.org/tutorials/images/classification
# https://www.keras.io/examples/vision/image_classification_from_scratch/
# The code in "plant_api.py" was written by the author with reference to official TensorFlow and Keras documentation.
# Some elements, such as image preprocessing and model loading, were adapted from common examples and tutorials for deploying deep learning models.

# Import necessary libraries
# os is used to locate the model file.
# io.BytesIO is used to read the raw bytes of the uploaded image.
import os
from io import BytesIO

# numpy is used for numerical operations, especially for handling image data.
# tensorflow is used for loading the Keras model and running inference.
# PIL (Pillow) is used for image processing, specifically to open and manipulate images.
import numpy as np
import tensorflow as tf
from PIL import Image

# — Step 1: locate & load the .keras model —
# The model was trained using TensorFlow 2.12.0 and Keras 2.12.0.
# The model file is located in the "model" directory
script_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(script_dir, os.pardir, "model")
model_path = os.path.join(model_dir, "plant_classifier.keras")
_model = tf.keras.models.load_model(model_path)

# — Step 2: class names in the same order as the training folders —
# The model was trained on a dataset with five classes:
# "edible", "flower", "grass", "succulent", and "tree".
_CLASS_NAMES = ["Edible", "Flower", "Grass", "Succulent", "Tree"]

# — Step 3: define the function to classify the image —
# This function accepts the raw bytes of an uploaded plant image, preprocesses it, runs inference, and returns one of the five class labels.
# The model only accepts images of size 224x224 pixels, so the function resizes the image accordingly.
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