# TUTORIAL ON HOW TO RUN THE APP, DOWNLOAD IMAGES AND TRAIN THE MODEL

# --- WARNING ---
# Our access to the weather API is based on a free trial account, it expires on May 23rd and requests are limited to 1000, if you run the app too many times or use the "Next Week" or "Previous Week" buttons too many times, you will run out of requests and receive an error message. 
# If this happens before you were able to test the website enough for the grading, please contact us.

# --- how to run the app: ---

#step 1
# open terminal on your computer

#step 2
# go in the specific folder in your terminal:
# (e.g. you have it in your Download file)
# type in your terminal: cd Download
# press enter
# type in your terminal: cd Plantelligence
# press enter

#step 3
# install streamlit and all the libraries from requirements.txt
# type in your terminal: pip install -r requirements.txt
# press enter

#step 4
# run the app on streamlit:
# type in your terminal: streamlit run app/app.py
# press enter

#step 5
# download plant images and have fun with the app!


# --- how to train the model ---
# We have sent you the project with the model trained, however, if you want to train the model and try the app again with the new model, please follow these steps

#step 1
# delete plant_classifier.keras file in the subfolder 'model'
# we encourage you to copy and paste it out of the Plantelligence folder to save it before you delete it

#step 2
# copy step 1 and 2 from before to get in the right folder of your terminal

#step 3
# create a new environment with conda
# type in your terminal: conda create -n plantelligence python=3.9
# press enter

# and install the libraries from requirements.txt
# type in your terminal: conda activate plantelligence
# press enter
# type in your terminal: pip install -r requirements.txt

#step 4
# type in your terminal: python model/predict.py
# press enter
# wait for the model to be trained and automatically saved in the 'model' subfolder (takes a few minutes depending on the processing power of your computer)

#step 5
# do steps 1 to 5 again from 'how to run the app' to try the app again with the model you just trained

# --- how to download images ---
# We have sent you the project with the images already downloaded, however, if you want to download the images and try the app again with the new images, please follow these steps
# However, we recommend to use the images we provided you with, as the ones downloaded from the API are not always the best quality and would need to be filtered
# if you want to download the images, please follow these steps:

#step 1
# create a folder called downloaded_plant_images in your Downloads folder

#step 2
# open terminal on your computer

#step 2
# go in the specific folder in your terminal:
# (e.g. you have it in your Download file)
# type in your terminal: cd Download
# press enter
# type in your terminal: cd Plantelligence
# press enter

#step 3
# run the Download_images.py script::
# type in your terminal: pyhton downloading_plant_images_from_Trefle/Download_images.py
# press enter