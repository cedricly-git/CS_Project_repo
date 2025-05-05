import tensorflow as tf
import numpy as np
import io
from PIL import Image

# --- Load the trained model once at import time ---
# This path is relative to your project root when you run:
#    streamlit run app/app.py
MODEL_PATH = "model/plant_classifier.keras"
model = tf.keras.models.load_model(MODEL_PATH)

# --- Class names (must match the folders you used when training) ---
# Keras orders classes alphabetically by folder name.
# Our folders were: Cacti_Succulents, Ferns_Mosses, Flowering_Plants,
# Fruiting_Plants, Grasses_Lawns, Trees_Shrubs
RAW_CLASS_NAMES = [
    "Cacti_Succulents",
    "Ferns_Mosses",
    "Flowering_Plants",
    "Fruiting_Plants",
    "Grasses_Lawns",
    "Trees_Shrubs"
]

# Convert to display-friendly names:
# e.g. "Cacti/Succulents", "Ferns/Mosses", etc.
PLANT_CATEGORIES = [cn.replace("_", "/") for cn in RAW_CLASS_NAMES]


def classify_plant_image(image_file) -> str:
    """
    Accepts an uploaded image (streamlit UploadedFile) and returns
    one of the six plant categories, or "Unknown" on error.
    """
    try:
        # 1) Load & convert to RGB
        image = Image.open(image_file).convert("RGB")

        # 2) Resize to training size
        image = image.resize((224, 224))

        # 3) Turn into numpy array, normalize to [0,1]
        img_array = tf.keras.utils.img_to_array(image) / 255.0

        # 4) Add batch dimension: (1, 224,224,3)
        img_array = np.expand_dims(img_array, axis=0)

        # 5) Run inference
        preds = model.predict(img_array)

        # 6) Get index of highest score
        pred_index = int(np.argmax(preds[0]))

        # 7) Map to your friendly category
        return PLANT_CATEGORIES[pred_index]

    except Exception as e:
        # In case anything goes wrong, log it and return Unknown
        print(f"[plant_api] classification error: {e}")
        return "Unknown"