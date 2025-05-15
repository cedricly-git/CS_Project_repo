# TUTORIAL ON HOW TO RUN THE APP AND TRAIN THE MODEL

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