import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

# === Step 1: Load the trained model ===
model_path = "/Users/graceyan/Downloads/St.Gallen /STUFF/plant_classifier3.keras"
model = tf.keras.models.load_model(model_path)
print("✅ Model loaded successfully.")

# === Step 2: Manually define class names (same order as in training) ===
class_names = ['Edible', 'Flower', 'Grass', 'Succulent', 'Tree']  # <-- Replace this list with your actual labels

# === Step 3: Prediction function ===
def predict_plant(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)[0]
    top_indices = predictions.argsort()[-3:][::-1]
    top_labels = [(class_names[i], predictions[i] * 100) for i in top_indices]

    print("\nTop Predictions:")
    for label, confidence in top_labels:
        print(f"{label}: {confidence:.2f}%")

    # Plot image with top prediction
    plt.imshow(img)
    plt.title(f"{top_labels[0][0]} ({top_labels[0][1]:.2f}%)")
    plt.axis('off')
    plt.show()

    return top_labels[0][0]

# === Step 4: Predict your image ===
image_path = "/Users/graceyan/Downloads/St.Gallen /STUFF/pics/160189097_7b64d32743_c.jpg"  # Change to your test image path
final_prediction = predict_plant(image_path)
print(f"\n✅ Final prediction: {final_prediction}")

