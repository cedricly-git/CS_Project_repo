# --- app.py ---
# This is the main application file for Plantelligence, a plant care assistant.
# It allows users to add plants, view their garden, and get weekly watering schedules based on weather data and their location.
# The app uses Streamlit for the frontend, Altair for visualizations, and integrates with various APIs for plant classification, calendar visualisaiton, and weather data.


# --- References & Credits ---
# Streamlit for building interactive web apps
# https://streamlit.io
# PyPI: https://pypi.org/project/streamlit/

# pandas for data analysis and manipulation
# https://pandas.pydata.org
# PyPI: https://pypi.org/project/pandas/

# datetime - built-in Python module for handling dates and times
# https://docs.python.org/3/library/datetime.html

# io - built-in Python module for handling streams (used here for in-memory file handling)
# https://docs.python.org/3/library/io.html

# Pillow (PIL) - Python Imaging Library for image processing
# https://python-pillow.org
# PyPI: https://pypi.org/project/Pillow/

# Altair - declarative statistical visualization library for Python
# https://altair-viz.github.io
# PyPI: https://pypi.org/project/altair/

# base64 - built-in Python module for base64 encoding/decoding
# https://docs.python.org/3/library/base64.html

# Real Pyhton tutorials: https://realpython.com
# W3Schools Python tutorial: https://www.w3schools.com/python/ 

# CSS documentation - styling cards and widget
# CSS reference: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference

# This project uses or was assisted by OpenAI's language models (ChatGPT/GPT-4)
# https://openai.com

# --- Project Structure ---
# ├── app.py                # Main application file
# ├── plant_api.py          # Plant classification API
# ├── weather_api.py        # Weather data API
# ├── calendar_api.py       # Calendar and scheduling API
# ├── model (folder)        # the code for training model & the .keras file, the trained model
# ├── requirements.txt      # Python package dependencies

# --- Import necessary libraries ---
# We use Streamlit for the web app, datetime for date handling, pandas for data manipulation,
# We use datetime and timedelta for date calculations, BytesIO for in-memory file handling,
# We use pandas for data manipulation, and PIL for image processing.
# We use altair for data visualization, and base64 for encoding images.
# We use base64 for encoding images.
import streamlit as st
import datetime
import pandas as pd
from datetime import timedelta
from io import BytesIO
from PIL import Image
import altair as alt
import base64

# --- Import custom modules ---
# The modules represent the different functionalities of the app
# Such as plant classification, weather data retrieval, and scheduling
from plant_api import classify_plant_image
from weather_api import get_weekly_rainfall, geocode
from calendar_api import get_watering_schedule

# --- Page config ---
# This sets the title and layout of the Streamlit app.
st.set_page_config(page_title="Plantelligence 🌱", layout="centered")

# --- Session State Init ---
# This initializes the session state variables to store user inputs and app data.
if 'garden' not in st.session_state:
    st.session_state.garden = []
if "plant_counters" not in st.session_state:
    st.session_state.plant_counters = []
if 'week_start' not in st.session_state:
    today = datetime.date.today()
    monday = today - timedelta(days=today.weekday())
    st.session_state.week_start = monday
if "checklist_states" not in st.session_state:
    st.session_state.checklist_states = {}

# --- App Title ---
# This sets the title of the app and allows the user to input the name of their garden.
# Title
st.title("Welcome to Plantelligence 🌱")
garden_name = st.text_input("Name your garden:", key="garden_name")
# allow the user to choose a city for the forecast in the sidebar
# defines the variables lat and lon based the city named (retrieve the geocode used later from the weather API directly)
with st.sidebar:
    st.header("Weather Settings 🌍")
    city = st.text_input("In which city is your garden?:", value="St. Gallen")
lat, lon = geocode(city)

# --- Add Plant Form ---
# This section allows the user to add a new plant to their garden.
# Title
st.subheader("🪴 Add a Plant to Your Garden")
# This block allow the user to name their plant, upload an image of it and submit so it gets analysed and displayed in the garden
with st.form("add_plant_form", clear_on_submit=True):
    plant_name = st.text_input("Plant Name", key="plant_name_input")
    plant_file = st.file_uploader("Upload Plant Image", type=["jpg", "jpeg", "png"], key="plant_file_input")
    submitted = st.form_submit_button("Add Plant")

 # --- Plant Classification ---
# This section classifies the uploaded plant image.
# Uses classify_plant_image from plant_api to determine the plant's type.
# First, the name or the image hasn't been uploaded, they get asked
# Otherwise, the image read, the type is determined, the plant is added to the garden with name, type and image, the plant counter increases, the plant is displayed with name, type and image, and finally the success message.
if submitted:
    if not plant_name or not plant_file:
        st.warning("Please provide both a plant name and an image.")
    else:
        image_bytes = plant_file.read()
        plant_type = classify_plant_image(image_bytes)
        display_img = Image.open(BytesIO(image_bytes)).convert("RGB")
        st.session_state.garden.append({
            "name": plant_name,
            "type": plant_type,
            "image_bytes": image_bytes
        })
        # starting of dry day counter for new plant; counter tracks how many days have passed without precipitation, whereby starting point is 0 days. 
        st.session_state.plant_counters.append(0)
        # clear watering schedule as the garden respectively the plants have changed (cache must is cleared).
        if 'cached_schedules' in st.session_state:
            st.session_state.cached_schedules = {}

# --- Garden Overview ---
# This section displays the user's garden overview, including the plants added and their types.
# We used CSS documentation and chat GPT for this section
if st.session_state.garden:
    st.markdown("<hr style='margin-top:50px; margin-bottom:20px;'>", unsafe_allow_html=True) # space for appearance
    title = f"🔍 Garden Overview 🔍: {garden_name}" if garden_name else "🔍 Garden Overview"#Title (of section AND name of the garden entered at the beginning)
    st.subheader(title)

    type_icons = {"Tree": "🌳", "Flower": "🌸", "Grass": "🌱", "Edible": "🥕", "Succulent": "🌵"} # define how the types will be displayed
    # format of the plants in the garden overview -> card view
    st.markdown(""" 
        <style>
        .plant-card {
            border: 1px solid #ddd;
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            background-color: #f9f9f9;
            transition: transform 0.2s;
        }
        .plant-card:hover {
            transform: scale(1.05);
            box-shadow: 4px 4px 15px rgba(0,0,0,0.2);
        }
        </style>
    """, unsafe_allow_html=True)

    num_cols = 3 # display plants in 3 columns with image, name, type in card forma
    cols = st.columns(num_cols)
    for idx, plant in enumerate(st.session_state.garden):
        with cols[idx % num_cols]:
            image = plant["image_bytes"]
            name = plant["name"]
            plant_type = plant["type"]
            icon = type_icons.get(plant_type, "🪴")
            base64_image = base64.b64encode(image).decode()
            st.markdown(f"""
                <div class="plant-card">
                    <img src="data:image/jpeg;base64,{base64_image}" width="150" style="border-radius:10px;"><br><br>
                    <strong style="font-size:16px;">{name}</strong><br>
                    <span style="color:gray; font-size:14px;">{icon} {plant_type}</span>
                </div>
            """, unsafe_allow_html=True)

    # --- Weekly Rainfall Forecast Section ---
    # This section displays the weekly rainfall forecast.
    # space for appearance
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    # Title
    st.subheader("Weekly Rainfall Forecast 🌧️")
    # This blocks display the "Previous Week" and "Next Week" buttons. These change the date of the week start when clicked.
    col1, col2 = st.columns([1, 3])

    with col1:
        if st.button("← Previous Week", key="prev_week"):
            st.session_state.week_start -= datetime.timedelta(days=7)

    with col2:
        if st.button("Next Week →", key="next_week"):
            st.session_state.week_start += datetime.timedelta(days=7)
            
    week_start = st.session_state.week_start
    
    # Week label
    # This section displays the week label based on the selected week start date.
    #define week start and end to be displayed
    wk_start = st.session_state.week_start
    wk_end   = wk_start + datetime.timedelta(days=6)
    # diplay week label with week start, end and year in the center
    st.markdown(
        f"<div style='text-align:center; font-weight:bold;'>"
        f"Week of {wk_start.strftime('%B')} {wk_start.day} – "
        f"{wk_end.strftime('%B')} {wk_end.day}, {wk_end.year}"
        f"</div>",
        unsafe_allow_html=True,)
    
    # source: ChatGPT assisted in the creation of the function and section concept and implementation. 
    # This section calculates and displays the weekly rainfall forecast chart based on the rainfall forecast.
    # fetch rainfall
    # This section fetches the weekly rainfall data with get_weekly_rainfall (function defined in weather_api.py)
    try:
        weekly_rain = get_weekly_rainfall(st.session_state.week_start, lat, lon)
    except Exception as e:
        # if fetching the precipitation forecast fails, an error message and indication of no rain is shown to the user.
        st.error(f"Error fetching weather data: {e}")
        weekly_rain = [0.0] * 7

    # Calculate watering schedule
    # This section checks if the watering schedule needs to be recalculated based on the week start date.
    # If the week start date has changed, recalculate the schedule.

    # conversion of the week start date into a string to use for caching.
    week_key = str(st.session_state.week_start)

    # checks whether the session state has a cache for the watering schedules. If such is not the case, an empty dictionary to store the cached schedules is initialised. 
    if 'cached_schedules' not in st.session_state:
        st.session_state.cached_schedules = {}
        
    # checking of if a schedule has already been calculated and stores for the present week. If such is the case, the schedule and the corresponding plant counters are retrieved from the cache. 
    if week_key in st.session_state.cached_schedules:
        schedule_df, counters = st.session_state.cached_schedules[week_key]

    # If this is not the case, a new watering schedule is calculated. Attempt to reuse any previously stored counters; if not then default to 0. 
    else:
        # Start counters for the week; use zeros if no previous data
        counters = st.session_state.cached_schedules.get(week_key, (None, [0] * len(st.session_state.garden)))[1]

        # calling of the scheduling function to determine which of the plants need watering for each of the week days. 
        schedule_df, counters = get_watering_schedule(
            st.session_state.garden, # present list of plants in garden
            weekly_rain, # precipitation forecase for week
            st.session_state.week_start, # start date of the present week
            counters  # Pass week-specific counters! # counter of dry days to maintain the indiviudal watering need of the respective plants
        )
        # storing of the newly computed schedule and counters in the cache for this week
        st.session_state.cached_schedules[week_key] = (schedule_df, counters)

    # Store final schedule and counters for use in this session
    st.session_state.watering_schedule = schedule_df
    st.session_state.plant_counters = counters

    # Chart
    # use the package altair to create a bar chart
    # This section creates a bar chart to visualize the weekly rainfall data.
    # Get the order of days from the DataFrame
    days_order = st.session_state.watering_schedule["Day"].tolist() # Get the order of days from the DataFrame
    # Create chart data from watering_schedule, with the days on the x axis and mm of rain on the y axis
    chart = (
        alt.Chart(st.session_state.watering_schedule)
          .mark_bar()
          .encode(
              x=alt.X("Day", sort=days_order, title="Day"),
              y=alt.Y("Rain (mm)", title="Rain (mm)"),
          )
    ) 
    # Display the chart
    st.altair_chart(chart, use_container_width=True) # Display the chart with altair
    
    # space for appearance
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    # --- Weekly Watering Schedule Table ---
    # This section displays the weekly watering schedule in a table format.
    # The table includes the day, date, rainfall amount, watering advice, and a personal checklist.
    # Title
    st.subheader("📅 Weekly Watering Schedule")
    # The variables are displayed in columns for column 0 we have the day, column 1 the date, column 2 the rain amount, column 3 the watering advice and column 4 a personal checklist
    header_cols = st.columns([2, 2, 2, 3, 2])
    header_cols[0].write("**Day**")
    header_cols[1].write("**Date**")
    header_cols[2].write("**Rain (mm)**")
    header_cols[3].write("**Watering Advice**")
    header_cols[4].write("**Personal Checklist**")
    # Add line after header
    st.markdown("<hr style='border: 1px solid #ddd; margin: 5px 0;'>", unsafe_allow_html=True) 

    #   This section iterates through the watering schedule DataFrame and displays each row in a column format.
    for idx, row in st.session_state.watering_schedule.iterrows(): 
        cols = st.columns([2, 2, 2, 3, 2])
        cols[0].write(row["Day"])
        cols[1].write(row["Date"])
        cols[2].write(f"{row['Rain (mm)']} mm")
        cols[3].write(row["Watering Advice"])

        # Personal checklist
        # This section creates a personal checklist for each day of the week in the 4th column.
        checked = cols[4].checkbox(
            label="",
            value=st.session_state.checklist_states.get(week_key, [False]*7)[idx],# Checks if the current week is in the checklist_states dictionary and gets the value for the current day.
            key=f"personal_check_{week_key}_{idx}" # Creates a unique key for each checkbox based on the week and day index.
        )
        # Update checklist state on user interaction
        if week_key not in st.session_state.checklist_states: # Checks if the checklist_states dictionary does not yet contain an entry for the current
            st.session_state.checklist_states[week_key] = [False]*7 # If the week is new, it initializes a checklist with 7 False values, one for each day of the week.
        st.session_state.checklist_states[week_key][idx] = checked # Updates the checklist for the current week, marks the specific day as checked or unchecked based on user input.
        
        # Add line after each row
        st.markdown("<hr style='border: 1px solid #eee; margin: 5px 0;'>", unsafe_allow_html=True)

else:
    st.info("📷 Please add at least one plant to your garden above.") # tell the user to add a plant if none are added


# --- Overlay Widget ---
# This section adds a floating widget to display the garden statistics.
# The widget displays the total number of plants, weeks tracked, current week, and tasks completed this week.
# We use CSS documentation and ChatGPT assistance to create this floating widget

# This block calculates the statistics for the floating widget.
total_plants = len(st.session_state.garden)
total_weeks = len(st.session_state.get("checklist_states", {}))
current_week = st.session_state.week_start.strftime("%B %d, %Y")
completed_tasks = sum(
    st.session_state.checklist_states.get(str(st.session_state.week_start), [])
) if "checklist_states" in st.session_state else 0

# This section creates the floating widget with the garden statistics.
st.markdown("""
    <style>
    .block-container {
        margin-right: 350px;  /* Moves the content left but keeps full width */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <style>
    .floating-widget {{
        position: fixed;
        top: 100px;
        right: 30px;
        width: 280px;
        padding: 20px;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        z-index: 100;
        font-family: 'Helvetica Neue', sans-serif;
    }}
    .floating-widget h4 {{
        color: #333333;
        font-size: 20px;
        margin-bottom: 20px;
    }}
    .floating-widget p {{
        margin: 8px 0;
        color: #555555;
        font-weight: 500;
        font-size: 15px;
    }}
    </style>

    <div class="floating-widget">
        <h4>📊 {garden_name if garden_name else "Garden Overview"}'s Statistics</h4>
        <p>Total Plants: {total_plants}</p>
        <p>Weeks Tracked: {total_weeks}</p>
        <p>Current Week:<br>{current_week}</p>
        <p>Tasks Completed This Week: {completed_tasks}</p>
    </div>
""", unsafe_allow_html=True)
