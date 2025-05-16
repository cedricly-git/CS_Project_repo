#In this script we are training the model to classiy plant images that we input, and then recognising it as one of 5 plant types: Flower, Grass, Edible, Tree, Succulent.
#We do this based on the plant’s visual characteristics that can be seen in the image. For this we have used a Convolutional Neural Network (CNN), 
#a neural network that specializes in working with visual data. Therein, it analyses and processes colors, textures, shapes, and much more of the 5 different plant types. 
#CNN is particularly good at recognizing and capturing the spatial hierarchies image features. That is, it first detects simple patterns in early layers, which are later combined into difficult and complex shapes in deeper layers. 


#importing libraries
import os
import tensorflow as tf #main Machine Learning framework we used for our model 
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import matplotlib.pyplot as plt
#source: 
# Official documentation: https://docs.python.org/3/library/os.html
# Official documentation: https://www.tensorflow.org/api_docs
# Official documentation: https://www.tensorflow.org/api_docs/python/tf/keras
# Official documentation: https://www.tensorflow.org/api_docs/python/tf/keras/callbacks
# Official documentation: https://matplotlib.org/stable/api/pyplot_api.html
# This implementation follows the TensorFlow image classification tutorial:
# https://www.tensorflow.org/tutorials/images/classification (Accessed: May 3, 2025)
# Function concept and implementation assisted by ChatGPT (Accessed: May 3 2024)

script_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(script_dir, os.pardir, "model")
model_path = os.path.join(model_dir, "plant_classifier.keras")
data_dir = os.path.join(script_dir, os.pardir, "plant_images") #Here, we specfify where the plant images are, i.e. the path to the image subfolders 


img_size = (224, 224) #we are specifyign the size of the images to 224x224 pixels, which all images will be resized to 
batch_size = 8 #this is the number of images processed at once
#source: 
# This implementation follows the TensorFlow image classification tutorial:
# https://www.tensorflow.org/tutorials/images/classification (Accessed: May 3, 2025)
# Function concept and implementation assisted by ChatGPT (Accessed: May 3 2024)

#Firstly, we have to create a Training Dataset, i.e. the set of images that will be used to train the dataset.
train_ds = tf.keras.preprocessing.image_dataset_from_directory( #using TensorFlow Keras
    data_dir, #specifiying the path to the images specified above
    validation_split=0.2, #80% of the images will be used for training the model 
    subset="training", #loading the "training" subset, as opposed to the validation/testing subset
    seed=123, #ensuring that splits stay the same throughout each run
    image_size=img_size, #image size as defined above 
    batch_size=batch_size #batch size as defined above 
)
#source: 
# This implementation follows the TensorFlow image classification tutorial:
# https://www.tensorflow.org/tutorials/images/classification (Accessed: May 3, 2025)


#Secondly, we need to create a Validation/Testing Dataset, i.e. the set of images that will be used to test how accurate the model is. 
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir, #specifiying the path to the images specified above
    validation_split=0.2, #20% of the images will be used for validating/testing the model 
    subset="validation", #loading the "validation" subset
    seed=123, #ensuring that splits stay the same throughout each run
    image_size=img_size, #image size as defined above 
    batch_size=batch_size #batch size as defined above 
)
#source: 
# This implementation follows the TensorFlow image classification tutorial:
# https://www.tensorflow.org/tutorials/images/classification (Accessed: May 3, 2025)


#when we loaded the dataset, TensorFlow automatically assigned calss lables based on the subfolders names, these are displayed here: 
class_names = train_ds.class_names #returns a list of the class labels, i.e. the plant types 
print(f"Detected classes: {class_names}")
#source: 
# This implementation follows the TensorFlow image classification tutorial:
# https://www.tensorflow.org/tutorials/images/classification (Accessed: May 3, 2025)

#We are now specifiying and optimising hwo the data will be loaded and given to the model. Since loading the data can be slow, we do the following: 
AUTOTUNE = tf.data.AUTOTUNE #this line assigns to AUTOTUNE that TensorFlow automatically decides on teh buffer size, i.e. how much data should be prepared in advance for the next batch of data ready to go, based on system resources. THis will be used for the next 2 lines.  
train_ds = train_ds.cache().shuffle(100).prefetch(buffer_size=AUTOTUNE) #The training set will be stored in RAM, randomizing 100 images at a time before giving them to the model for training, and starts preparing the next batch during training of the previous batch.  
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE) #we don't need to shuffle here, because validation is supposed to be consistent every run. 
#source: 
# This implementation follows the TensorFlow image classification tutorial:
# https://www.tensorflow.org/tutorials/images/classification (Accessed: May 3, 2025)

#Here we have to augment the images, meaning that we show the model slightly augmented versions of the plant images. We do this so that the model can generalize better. We are increasing the diversity of the images in our training data. 
data_augmentation = tf.keras.Sequential([ #a sequential pipeline is created, where each image will be passed through later, in this given order
    layers.RandomFlip("horizontal_and_vertical"), #randomly flips the image horizontally and vertically
    layers.RandomRotation(0.3), #randomly rotates the image by around 108 degrees (30% of 360 degrees)
    layers.RandomZoom(0.2), #randomly zooms in or out of the image by around 20%
    layers.RandomTranslation(0.1, 0.1), #randomly shifts the image along the x of y axes by around 10% of the original image size
    layers.RandomContrast(0.1), #randomly adjusts the image's contrast by around 10%
    layers.RandomBrightness(0.1), #randomly adjusts the image's brightness by around 10%
])
#source: 
# This implementation follows the TensorFlow image classification tutorial:
# https://www.tensorflow.org/tutorials/images/data_augmentation (Accessed: May 3, 2025)
# Function concept and implementation assisted by ChatGPT (Accessed: May 3 2024)

#Here we are building the CNN itself, this means that we are defining the sequence through so-called layers, through which the image will be passed 
model = models.Sequential([
    data_augmentation,  #here we are using the data augmentation pipeline during training which are being applied to the images, as we defined before
    layers.Rescaling(1./255, input_shape=(224, 224, 3)), #we are normalising the pixel values to 0,1, i.e. dividing it by 255. This helps the model have a more stable training. 
    layers.Conv2D(32, 3, activation='relu'), #this applies 32 filters, i.e. feature detectors over the image, each with a size of 3x3, these then slide over the image to recognise "low-level" pattern, such as lines, colors and basic shapes. Also, it only keeps positive patterns detected. 
    layers.MaxPooling2D(), #this keeps only the most important feature of each of the feature detectors, this is because it keeps the computations small, i.e. more managable
    layers.Conv2D(64, 3, activation='relu'), #now 64 filters are being applied, i.e. the model is recognising more complex features in the pictures, such as curves and textures. 
    layers.MaxPooling2D(), #again, only the most important features are kept
    layers.Conv2D(256, 3, activation='relu'), #now 256 filters are being applied, to recognise even more complex features, i.e. entire plant shapes, and even thorns of a cactus, etc.
    layers.MaxPooling2D(), #again
    layers.Flatten(), #Now, the final output will be converted to a 1D flat vector, this is because the in the next steps 1D vector inputs are expected
    layers.Dense(128, activation='relu'), #A so-called neural layer with 128 neurons, whereby each neuron looks at all the features that were kept from before and "tries" to extract meaningful information out of them for plant classficiation later. 
    layers.Dropout(0.5), #increased from 0.1 to 0.3 to now 0.5. Here 50% of the neurons are turned of, so that the model doesn't rely on the strongest neurons, this is to prevent overfitting, making it more robust. 
    layers.Dense(len(class_names), activation='softmax') #Here, each there is one neuron per class, i.e. 5, each associated with probability, the strongest probability indicates the confidence level of the model in that classification prediction. 
])
#source: 
# This implementation follows the TensorFlow image classification tutorial:
# https://www.tensorflow.org/tutorials/images/data_augmentation (Accessed: May 3, 2025)
# Function concept and implementation assisted by ChatGPT (Accessed: May 3 2024)

model.compile( #here we specifiy 3 components that are important for the training of the model 
    optimizer='adam', #controls how the model updates its weights, through caculating weight updatse using averages, i.e. hwow much weight in terms of important is given to each feature that has been detected.
    loss='sparse_categorical_crossentropy', #a formula that calculates how wrong the model's prediction are, which the model is trying to minimize
    metrics=['accuracy'] #this specifies how a "success" is reported in the model, and we choose accuracy, 
)
#source: 
# This implementation follows the TensorFlow image classification tutorial:
# https://www.tensorflow.org/tutorials/images/transfer_learning (Accessed: May 3, 2025)
# Function concept and implementation assisted by ChatGPT (Accessed: May 3 2024)

#setting up some callbacks:
callbacks = [
    EarlyStopping(patience=10, restore_best_weights=True), #it stops training early if the model's performance stops improving for 10 epochs
    ModelCheckpoint(filepath=model_path, save_best_only=True), #locally saving the trained model, filepath might have to be adjusted
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6, verbose=1) #reduces the learning rate by half when the model stops improving. It is based on the validation loss.
]
#source: 
# Function concept and implementation assisted by ChatGPT (Accessed: May 3 2024)

#This is the actual training loop. A batch of images is taken from the training set, which is then passed through the CNN layers, whereby predictions are made about the images in the last layer. Then, the predictions are compared to their true labels using the the loss function under model.compile()
#Thereon, the model is validated to and the validation loss and accuracy are calculated. Lastly, the callbacks that we specfied earlier are being checked. This process repeats for each epoch. 
history = model.fit(
    train_ds, #this is the training set that the model is trained with, containing 1) images and 2) labels (true plant types)
    validation_data=val_ds, #this is the validation/test dataset
    epochs=1, #looping through the training set 50 times 
    callbacks=callbacks
)
#source: 
# This implementation follows the TensorFlow image classification tutorial:
# https://www.tensorflow.org/tutorials/images/data_augmentation (Accessed: May 3, 2025)

#Evaluating the model
#finally, we a using matplotlib to visualize the model's accuracy over each epoch for training and validation.
plt.plot(history.history['accuracy'], label='Train Accuracy') #plots the training accuracy
plt.plot(history.history['val_accuracy'], label='Validation Accuracy') #plots the validation accuracy
plt.title("Training Progress") #Title of the graph 
plt.xlabel("Epoch") #x axis labelling 
plt.ylabel("Accuracy") #y axis labelling 
plt.legend() #adds a legend with Train Accuracy and Validation Accuracy
plt.grid(True) #adds a grid
plt.show() #displays the plot 
#source: 
# This implementation follows the TensorFlow image classification tutorial:
# https://www.tensorflow.org/tutorials/images/classification (Accessed: May 4, 2025)
# Function concept and implementation assisted by ChatGPT (Accessed: May 4 2024)

print(model_path)