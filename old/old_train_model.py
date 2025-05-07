import os
import tensorflow as tf

# === Step 1: Define paths and parameters ===
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "plant_images")  # training images directory
img_height = 224
img_width = 224
batch_size = 8
epochs = 10
seed = 123

# === Step 2: Load training and validation data ===
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=seed,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    label_mode="int"   # labels as integer indices
)
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=seed,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    label_mode="int"
)

# Save the class names (should be ['Edible', 'Flower', 'Grass', 'Succulent', 'Tree'])
class_names = train_ds.class_names
print(f"Classes found: {class_names}")

# === Step 3: Prepare dataset for performance ===
# Cache and prefetch for faster training, shuffle training data
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(100).prefetch(buffer_size=AUTOTUNE)
val_ds   = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# === Step 4: Build the CNN model ===
# Data augmentation layer (applied only during training)
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.1),
    tf.keras.layers.RandomContrast(0.1),
    # tf.keras.layers.RandomBrightness(0.1)  # (optional) uncomment if using TF >= 2.10
])
# Determine number of classes from the dataset
num_classes = len(class_names)

model = tf.keras.Sequential([
    data_augmentation,  # apply augmentations
    tf.keras.layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),  # normalize pixels
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(128, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),  # reduce overfitting
    tf.keras.layers.Dense(num_classes, activation='softmax')  # output layer
])

# === Step 5: Compile the model ===
model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),  # suitable for integer labels
    metrics=['accuracy']
)

# (Optional) Print a summary of the model architecture
model.summary()

# === Step 6: Train the model ===
print(f"\nStarting training for {epochs} epochs...")
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
)

# === Step 7: Save the trained model ===
# Ensure the target directory exists
model_dir = os.path.join(script_dir, "model")
os.makedirs(model_dir, exist_ok=True)
model_save_path = os.path.join(model_dir, "plant_classifier.keras")
model.save(model_save_path)
print(f"\nModel training complete. Saved the model to {model_save_path}")