"""
Plant Image Classifier Training Script

This script trains a convolutional neural network (CNN) to classify plant images into 6 categories:
Cacti/Succulents, Grasses/Lawns, Flowering Plants, Fruiting Plants, Trees/Shrubs, and Ferns/Mosses.

Usage:
1. Ensure you have a directory named 'plant_images' at the project root. Inside 'plant_images', 
   create six subfolders (one for each class) and place the training images accordingly. 
   For example:
       plant_images/Cacti_Succulents/  (images of cacti or succulents)
       plant_images/Grasses_Lawns/     (images of grass or lawn plants)
       plant_images/Flowering Plants/  (images of flowering plants)
       plant_images/Fruiting Plants/   (images of fruit-bearing plants)
       plant_images/Trees_Shrubs/      (images of trees or shrubs)
       plant_images/Ferns_Mosses/      (images of ferns or mosses)
   *Note:* Use underscores or spaces in folder names instead of '/' if your OS does not allow 
   '/' in folder names. The important part is that there are exactly these six class subfolders.

2. Run this script (for example, `python train_model.py`). It will automatically split the images 
   into training and validation sets (80% training, 20% validation).

3. After training, the model is saved as 'plant_classifier.keras' in the 'model/' directory. 
   This single file contains the trained model architecture and weights and is ready for loading in the Streamlit app.
"""

# Step 1: Import necessary libraries
# ----------------------------------
import tensorflow as tf
import os

# Step 2: Define dataset path and parameters
# ------------------------------------------
# Define the path to the dataset directory (assuming script is in 'model' folder and images in '../plant_images')
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "plant_images")  # path to 'plant_images' folder

# Define the expected image size (height, width) and training parameters
img_height = 224   # you can adjust this (e.g., 180 or 224) depending on your needs
img_width  = 224
batch_size = 32
epochs     = 10    # number of training epochs (you can increase for better accuracy if needed)
validation_split = 0.2  # 20% of data will be used for validation

# Step 3: Load images from directory and create training/validation datasets
# --------------------------------------------------------------------------
# We use Keras utility to load images from the directory structure.
# It will infer class labels from the subfolder names and split the data into training and validation sets.
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=validation_split,
    subset="training",
    seed=123,  # seed for reproducibility of the train/val split
    image_size=(img_height, img_width),
    batch_size=batch_size
)
val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=validation_split,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

# Get the class names (should be the 6 categories) from the training dataset
class_names = train_ds.class_names
print("Class names found:", class_names)  # e.g., ['Cacti_Succulents', 'Ferns_Mosses', ...] (alphabetical order)

# Ensure the datasets are optimized for performance
# Cache the datasets in memory (if they fit) and prefetch for faster training
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds   = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# Step 4: Build the neural network model
# --------------------------------------
# We define a simple CNN model. The model consists of convolutional layers for feature extraction
# followed by dense layers for classification into 6 classes.
num_classes = len(class_names)  # this should be 6 if the data is set up correctly

model = tf.keras.Sequential([
    # Rescaling layer to normalize pixel values from [0,255] to [0,1]
    tf.keras.layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),

    # Convolutional base: a stack of Conv2D and MaxPooling2D layers
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(128, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),

    # Flatten the feature map to a 1D vector before the dense layers
    tf.keras.layers.Flatten(),
    # Fully connected layer for learning non-linear combinations of features
    tf.keras.layers.Dense(128, activation='relu'),
    # Dropout layer to reduce overfitting (randomly disable 50% of neurons in the dense layer during training)
    tf.keras.layers.Dropout(0.5),
    # Output layer with `num_classes` units (one per class) and softmax activation for multi-class prediction
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

# Step 5: Compile the model
# -------------------------
# We use a suitable optimizer and loss function for multi-class classification.
# SparseCategoricalCrossentropy is used since our labels are integers (if label_mode='int').
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])

# Print a summary of the model architecture
model.summary()

# Step 6: Train the model
# -----------------------
# Train the model using the training dataset, and validate on the validation dataset.
print("\nStarting training for {} epochs...".format(epochs))
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
)

# Step 7: Save the trained model
# ------------------------------
# After training, save the model to a file in Keras format.
# The .keras extension saves the model in a single file (including architecture and weights).
model_save_path = os.path.join(script_dir, "plant_classifier.keras")
model.save(model_save_path)
print(f"\nModel training complete. Saved the model to {model_save_path}")
