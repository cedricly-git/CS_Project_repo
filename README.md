**Plantelligence – Project Framework**

**Project Overview**

This Streamlit app helps users track plant watering needs by combining image-based plant classification with weather data. The user can upload a plant photo (assigning it a nickname) and the app will identify the plant type using a pre-trained ML model. Based on the plant type and recent rainfall from the Meteomatics API, the app displays a week-view calendar with daily rainfall (mm) and watering reminders. The goal is to solve the common problem of when to water different types of plants, by clearly showing if and when a plant needs watering given recent or forecast rain.

**Key Features:**
	•	Machine Learning Inference: Classify an uploaded plant image into one of six categories (Cacti/Succulents, Grasses/Lawns, Flowering Plants, Fruiting Plants, Trees/Shrubs, Ferns/Mosses) using a pre-trained model (placeholder integration).
 	•	Weather Data via API: Retrieve daily rainfall data (mm) for the selected location using the Meteomatics Weather API (free tier). This uses API calls with basic authentication to get JSON weather data.
  	•	Intuitive Week-View Calendar: Display a 7-day calendar (with navigation for previous/next weeks) showing each day’s rainfall and whether watering is recommended for the plant. Watering reminders follow rules for each plant type and consider the last significant rain event (e.g. a “significant rain” is defined as >10 mm in a day ￼).
   	•	Data Visualization: Include a simple bar chart of the week’s daily rainfall for a quick visual overview.
    	•	User Interaction: Interactive file upload for images and week navigation buttons. All state (plant info, current week) is stored in the Streamlit session (no database or login). Data resets on refresh.
     	•	Collaborative Codebase: The code is organized into clear modules with descriptive comments, making it easy for a team to collaborate. Each component (classification, weather API, scheduling logic, UI) is separated for clarity.

**Project Structure**

The project is organized into a folder structure that separates concerns and makes the codebase maintainable:
1. app
  -> app.py
  -> calendar_api.py
  -> plant_api.py
  -> weather_api.py
2. model
   -> plant classifier
3. workspace
   -> old stuff
4. README.MD
5. requirements.txt

	•	app/app.py: The main Streamlit app, orchestrating the UI. It handles user inputs (image upload, week navigation), calls the classifier and weather modules, and displays results (rain chart and calendar with reminders).
	•	app/calendar_api.py: Contains logic to determine watering advice for each day of the week given the plant type and rainfall. It encodes the rules for each plant category (as given in the project specs) to output “Water” or “No water needed” recommendations per day. This keeps scheduling logic separate from data retrieval.
	•	app/plant_api.py: Handles machine learning aspects. This module would load the pre-trained plant classification model and provide a function to predict the plant type from an image. (In this framework, a placeholder function is used, and integration hooks are clearly marked for adding the real model.)
	•	app/weather_api.py: Deals with fetching weather data from Meteomatics. It contains a function to retrieve a week’s daily precipitation (in mm) for a given location via the Meteomatics API (using basic auth and/or token). API credentials and endpoints are configured here (with placeholders for secure info).

Each Python file is well-commented to explain its purpose and the steps of the computation, making it easy for others to understand and contribute. Below, we provide code snippets for these components which can be copied directly into VS Code and run with Streamlit.

**app/app.py – Main Streamlit Application**
Notes on the main app code: This script creates the Streamlit interface. It uses a form to get the plant name and image, then calls the classifier to determine the plant type. The result (name & type) is stored in st.session_state so it persists while the user navigates through weeks. The week navigation is handled by adjusting a week_start date in session state; by default, it starts at the current week’s Monday. For each week, we fetch rainfall data and then generate watering advice using our helper modules. Finally, we display a bar chart of rainfall and a table that lists each day’s date, rainfall, and whether to water the plant or not on that day. The code is thoroughly commented to explain each section.

**app/plant_api.py – Plant Classification Module (ML Model Integration)**
Notes: This module is responsible for machine learning inference. In practice, you would load your pre-trained model (e.g., in model/plant_classifier.pth or a TensorFlow .h5 file) at the top. The classify_plant_image function takes the uploaded image file, processes it, and uses the model to predict the plant category. We included a placeholder implementation (always classifying as “Flowering Plants”) to allow the app to run without a real model. The code comments indicate where to insert actual model loading and prediction code. The list PLANT_CATEGORIES should match the classes that the model can predict. This separation allows a team member focusing on ML to work in this file independently.

**app/weather_api.py – Weather Data Integration Module**
Notes: This module handles communication with the Meteomatics API. The get_weekly_rainfall function builds a REST API query for daily precipitation from the given start date over a 7-day period (P1D interval). It uses the precip_24h:mm parameter which returns the total rainfall in the past 24 hours for each day. By default, it fetches data for a fixed location (latitude/longitude are set for St. Gallen, CH) – these can be changed or made dynamic (e.g., user input) in the future. API credentials are placeholders: in a real app, you should secure these (for example, via Streamlit Secrets or environment variables instead of hard-coding). The code uses basic HTTP authentication (requests.get(..., auth=(user, pass))). Meteomatics also offers an OAuth token flow (obtain a token via basic auth and use it in requests), but for simplicity we use direct basic auth for each request here. The function returns a list of 7 rainfall values (one per day). If the API response is not as expected or an error occurs, it raises an exception to be handled by the caller. This separation allows a team member to focus on the API integration details.

**app/calendar_api.py – Weekly Watering Schedule Logic**
Notes: This module encapsulates the watering reminder logic. The function get_watering_advice takes the plant type and the week’s rainfall data and returns a parallel list of advice strings for each day. It uses the guidelines from the provided table for each category:
	•	Cacti/Succulents: Very drought-tolerant – water roughly every 2–3 weeks if no rain (prefer dry conditions, so skip watering if any rain is in forecast).
	•	Grasses/Lawns: Need regular moisture – about 1–2 times per week if no rain (so if a week goes by with little rain, water).
	•	Flowering Plants: Sensitive to drying – water ~2–3 times a week in hot conditions if no rain for 3+ days.
	•	Fruiting Plants: Need a lot of water especially when fruiting – ~2–3 times a week unless a heavy rain occurred recently (>=10 mm).
	•	Trees/Shrubs: Deep but infrequent watering – roughly every 1–2 weeks if dry (so if ~10 days pass without significant rain, water).
	•	Ferns/Mosses: Love humidity – water very frequently (every 2–3 days if no rain; they thrive on constant moisture).

These rules are encoded via the max_dry_days for each type. The algorithm keeps track of how many consecutive days have passed without a significant rain (we define “significant” as ≥10 mm in a day, following common definitions ￼). If the dry spell exceeds the threshold for that plant type, it triggers a “Water” recommendation and resets the counter (assuming the act of watering would reset the dryness count). Otherwise, it advises “No water needed”. This is a simplified approach; in a real scenario, you might incorporate more factors (like temperature or soil moisture), but it meets the requirements for this student project. The clear separation here allows adjustment of watering rules without touching the rest of the app.

**Additional Considerations**
	•	Run the App: To run this app, install the dependencies listed in requirements.txt (such as streamlit, requests, pillow for image handling, etc.), then execute streamlit run app/app.py. The app will open in a browser for interaction.
	•	API Credentials: Remember to replace the Meteomatics METEO_USER and METEO_PASS placeholders with your actual API credentials. For security, you might use Streamlit’s secrets management instead of hard-coding these values in the weather_api.py file.
	•	Model Integration: Place your trained model file (if any) in the model/ directory and update the plant_api.py to load it. The placeholder classification currently always returns “Flowering Plants” – integrating the real model will provide actual predictions.
	•	Session State: All data (the plant info and the current week) is stored in session state, meaning if you add a plant and navigate weeks, it will remember the plant classification. However, if you refresh the app, the state clears (since there is no persistent storage by design).
	•	Collaboration: The code is organized and commented to facilitate teamwork. Each team member can work on a separate module (e.g., one on the ML model in plant_api.py, another on the Meteomatics integration in weather_api.py, etc.) without stepping on each other’s toes. The source code comments explain functionality in detail, which is crucial for collaborative development and future maintainability.
