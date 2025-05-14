# --- app.py ---
# This is the main application file for Plantelligence, a plant care assistant.
# It allows users to add plants, view their garden, and get weekly watering schedules based on weather data.
# The app uses Streamlit for the frontend, Altair for visualizations, and integrates with various APIs for plant classification and weather data.

# --- References & Credits ---
# Plant Image Classification Model:
# Adapted from the official [TensorFlow Image Classification Tutorial](https://www.tensorflow.org/tutorials/images/classification).

# Weather Data :
# Provided by [Meteomatics Weather API](https://www.meteomatics.com/en/).
# Geolocation powered by [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api).

# Scheduling & Checklist UI:
# Custom implementation for Plantelligence using [Streamlit](https://streamlit.io/).
        
# Altair Charting:
# Rainfall bar charts generated using [Altair](https://altair-viz.github.io/).
    
# Icons and Emojis inspired by [Emojipedia](https://emojipedia.org/) and modern UX design patterns.

# --- Import necessary libraries ---
import streamlit as st
import datetime
import pandas as pd
from datetime import timedelta
from io import BytesIO
from PIL import Image
import altair as alt
import base64

# --- Import custom modules ---
# the modules represent the different functionalities of the app
# such as plant classification, weather data retrieval, and scheduling
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
# This sets the title of the app and allows the user to name their garden.
st.title("Welcome to Plantelligence 🌱")
garden_name = st.text_input("Name your garden:", key="garden_name")
# allow the user to choose a city for the forecast
with st.sidebar:
    st.header("Weather Settings 🌍")
    city = st.text_input("In which city is your garden?:", value="St. Gallen")
lat, lon = geocode(city)

# --- Add Plant Form ---
# This section allows the user to add a new plant to their garden.
st.subheader("🪴 Add a Plant to Your Garden")
with st.form("add_plant_form", clear_on_submit=True):
    plant_name = st.text_input("Plant Name", key="plant_name_input")
    plant_file = st.file_uploader("Upload Plant Image", type=["jpg", "jpeg", "png"], key="plant_file_input")
    submitted = st.form_submit_button("Add Plant")

 # --- Plant Classification ---
# This section classifies the uploaded plant image and adds it to the garden.
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
        st.session_state.plant_counters.append(0)
        st.image(display_img, caption=f"{plant_type}: {plant_name}")
        st.success(f"Added **{plant_type}** “{plant_name}” to your garden.")

# --- Garden Overview ---
# This section displays the user's garden overview, including the plants added and their types.
# It also shows the weekly rainfall forecast and the watering schedule.
if st.session_state.garden:
    st.markdown("<hr style='margin-top:50px; margin-bottom:20px;'>", unsafe_allow_html=True)
    title = f"🔍 Garden Overview: {garden_name}" if garden_name else "🔍 Garden Overview"
    st.subheader(title)

    type_icons = {"Tree": "🌳", "Flower": "🌸", "Grass": "🌱", "Edible": "🥕", "Succulent": "🌵"}

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

    num_cols = 3
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
    # This section displays the weekly rainfall forecast and the watering schedule.
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    st.subheader("Weekly Rainfall Forecast 🌧️")

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
    wk_start = st.session_state.week_start
    wk_end   = wk_start + datetime.timedelta(days=6)
    st.markdown(
        f"<div style='text-align:center; font-weight:bold;'>"
        f"Week of {wk_start.strftime('%B')} {wk_start.day} – "
        f"{wk_end.strftime('%B')} {wk_end.day}, {wk_end.year}"
        f"</div>",
        unsafe_allow_html=True,)

# --- Weekly Watering Schedule ---
# This section calculates and displays the weekly watering schedule based on the rainfall forecast.
    # 1) make sure we have a persistent counters list in session state
    if "plant_counters" not in st.session_state:
        st.session_state.plant_counters = [0] * len(st.session_state.garden)

    # 2) fetch rainfall
    # This section fetches the weekly rainfall data from the weather API.
    try:
        weekly_rain = get_weekly_rainfall(st.session_state.week_start, lat, lon)
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        weekly_rain = [0.0] * 7

    # 3) Check if watering schedule needs to be recalculated
    # This section checks if the watering schedule needs to be recalculated based on the week start date.
    # If the week start date has changed, recalculate the schedule.
    week_key = str(st.session_state.week_start)
    if 'watering_schedule' not in st.session_state or st.session_state.watering_schedule_key != week_key:
        schedule_df, new_counters = get_watering_schedule(
            st.session_state.garden,
            weekly_rain,
            st.session_state.week_start,
            st.session_state.plant_counters
        )
        st.session_state.watering_schedule = schedule_df
        st.session_state.plant_counters = new_counters
        st.session_state.watering_schedule_key = week_key

    # 4) Chart
    # This section creates a bar chart to visualize the weekly rainfall data.
    days_order = st.session_state.watering_schedule["Day"].tolist()
    chart = (
        alt.Chart(st.session_state.watering_schedule)
          .mark_bar()
          .encode(
              x=alt.X("Day", sort=days_order, title="Day"),
              y=alt.Y("Rain (mm)", title="Rain (mm)"),
          )
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

    # --- Weekly Watering Schedule Table ---
    # This section displays the weekly watering schedule in a table format.
    # The table includes the day, date, rainfall amount, watering advice, and a personal checklist.
    # The variables are displaed in columns
    st.subheader("📅 Weekly Watering Schedule")
    header_cols = st.columns([2, 2, 2, 3, 2])
    header_cols[0].write("**Day**")
    header_cols[1].write("**Date**")
    header_cols[2].write("**Rain (mm)**")
    header_cols[3].write("**Watering Advice**")
    header_cols[4].write("**Personal Checklist**")

    # Add line after the header
    st.markdown("<hr style='border: 1px solid #ddd; margin: 5px 0;'>", unsafe_allow_html=True)

    #   This section iterates through the watering schedule DataFrame and displays each row in a column format.
    for idx, row in st.session_state.watering_schedule.iterrows():
        cols = st.columns([2, 2, 2, 3, 2])
        cols[0].write(row["Day"])
        cols[1].write(row["Date"])
        cols[2].write(f"{row['Rain (mm)']} mm")
        cols[3].write(row["Watering Advice"])

        checked = cols[4].checkbox(
            label="",
            value=st.session_state.checklist_states.get(week_key, [False]*7)[idx],
            key=f"personal_check_{week_key}_{idx}"
        )
        # Update checklist state on user interaction
        if week_key not in st.session_state.checklist_states:
            st.session_state.checklist_states[week_key] = [False]*7
        st.session_state.checklist_states[week_key][idx] = checked
        
        # Add line after each row
        st.markdown("<hr style='border: 1px solid #eee; margin: 5px 0;'>", unsafe_allow_html=True)

else:
    st.info("📷 Please add at least one plant to your garden above.")

# --- Overlay Widget ---
# This section adds a floating widget to display the garden statistics.

# This section adds CSS to style the floating widget.
st.markdown("""
    <style>
    .block-container {
        margin-right: 350px;  /* Moves the content left but keeps full width */
    }
    </style>
""", unsafe_allow_html=True)

# This section calculates the statistics for the floating widget.
total_plants = len(st.session_state.garden)
total_weeks = len(st.session_state.get("checklist_states", {}))
current_week = st.session_state.week_start.strftime("%B %d, %Y")
completed_tasks = sum(
    st.session_state.checklist_states.get(str(st.session_state.week_start), [])
) if "checklist_states" in st.session_state else 0

# This section creates the floating widget with the garden statistics.
# The widget displays the total number of plants, weeks tracked, current week, and tasks completed this week.
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

