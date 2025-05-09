# hardcode to test streamlit without ML (so to fix plant_api to return flower)

# import tensorflow as tf   # ← comment out for now
# import numpy as np

def classify_plant_image(image_file) -> str:
    """
    TEMPORARY STUB: ignore the image and always return the same category
    so we can test the app without a model.
    """
    return "Flower"
