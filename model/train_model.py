# --- Plant Image Classification Model Training ---
# This script trains a convolutional neural network (CNN) to classify plant images into different categories.
# The model is trained using TensorFlow and Keras, with data augmentation and model checkpointing.
# The dataset is expected to be organized in a directory structure where each subdirectory contains images of a specific class.

import os
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# Step 1: Define paths and parameters
# Define the path to the dataset and model directory
script_dir = os.path.dirname(os.path.abspath("train_model.py"))
data_dir = os.path.join(script_dir, os.pardir, "plant_images")
model_dir = os.path.join(script_dir, os.pardir, "model")
os.makedirs(model_dir, exist_ok=True)
checkpoint_path = os.path.join(model_dir, "plant_classifier.keras")
img_size = (224, 224)
batch_size = 8
epochs     = 10
seed       = 123

# Step 2: Load training and validation data
# Load the dataset from the directory
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)

# Load the validation dataset
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)

# Save the class names ("Edible", "Succulent","Grass" , "Tree", "Flower")
class_names = train_ds.class_names
print(f"Detected classes: {class_names}")

# Step 3: Set up data performance and augmentation
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(100).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# Data augmentation layer: random flip, rotation, zoom
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
    layers.RandomContrast(0.1),
    layers.RandomBrightness(0.1),
])

# Step 4: Build your CNN model
model = models.Sequential([
    data_augmentation,  # apply augmentations during training
    layers.Rescaling(1./255, input_shape=(224, 224, 3)),  # normalize
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(256, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),  # helps prevent overfitting
    layers.Dense(len(class_names), activation='softmax')  # output layer
])

# Step 5: Compile the model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau

callbacks = [
    ModelCheckpoint(
        filepath=checkpoint_path,
        save_best_only=True
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-6,
        verbose=1
    ),
]

# Step 6: Train the model
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=50,
    callbacks=callbacks
)

# Step 7: Plot training vs validation accuracy
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title("Training Progress")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)
plt.show()


#CONFUSION MATRIX

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Step 1: Get true labels and predicted labels
y_true = []
y_pred = []

for batch_images, batch_labels in val_ds:
    preds = model.predict(batch_images)
    y_true.extend(batch_labels.numpy())
    y_pred.extend(np.argmax(preds, axis=1))

# Build matrix
cm = confusion_matrix(y_true, y_pred)

# Plot
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()

# --- Reference ---
# https://www.tensorflow.org/tutorials/images/classification
# The code for training the plant image classification model was adapted from the official TensorFlow tutorial:"Image classification" (TensorFlow Tutorials).
# Modifications were made by the author to fit the specific dataset (plant_images), add data augmentation, implement model checkpointing, and generate a confusion matrix for performance evaluation.