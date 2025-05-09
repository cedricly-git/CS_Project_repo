# app/app.py

import streamlit as st
import datetime
import pandas as pd
from datetime import timedelta
from io import BytesIO
from PIL import Image
import altair as alt

from plant_api import classify_plant_image
from weather_api import get_weekly_rainfall, geocode
from calendar_api import get_watering_schedule

# --- Page config & session-state init --- 
st.set_page_config(page_title="Plantelligence", layout="centered")

if 'garden' not in st.session_state:
    st.session_state.garden = []

if "plant_counters" not in st.session_state:
    st.session_state.plant_counters = []

if 'week_start' not in st.session_state:
    today = datetime.date.today()
    monday = today - timedelta(days=today.weekday())
    st.session_state.week_start = monday

# --- Title & garden-name input ---
st.title("Welcome to Plantelligence 🌱")
garden_name = st.text_input("Name your garden:", key="garden_name")
# allow the user to choose a city for the forecast
city = st.text_input("In what city is your garden:", value="St. Gallen")
lat, lon = geocode(city)

# --- Add-plant form ---
st.subheader("Add a Plant to Your Garden 🪴")
with st.form("add_plant_form", clear_on_submit=True):
    plant_name = st.text_input("Plant Name", key="plant_name_input")
    plant_file = st.file_uploader(
        "Upload Plant Image", type=["jpg","jpeg","png"], key="plant_file_input"
    )
    submitted = st.form_submit_button("Add Plant")

if submitted:
    if not plant_name or not plant_file:
        st.warning("Please provide both a plant name and an image.")
    else:
        # 1) pull out the raw bytes
        image_bytes = plant_file.read()

        # 2) classify from the raw bytes stream
        plant_type = classify_plant_image(image_bytes)

        # 3) now open a PIL image just for showing it
        display_img = Image.open(BytesIO(image_bytes)).convert("RGB")

        st.session_state.garden.append({
            "name": plant_name,
            "type": plant_type,
            "image_bytes": image_bytes
        })
        st.session_state.plant_counters.append(0)
        st.image(display_img, caption=f"{plant_type}: {plant_name}")
        st.success(f"Added **{plant_type}** “{plant_name}” to your garden.")

# --- If we have at least one plant, show overview + charts ---
if st.session_state.garden:
    garden = st.session_state.garden

    # 1) Garden overview gallery
    title = f"Garden Overview 🔍: {garden_name}" if garden_name else "Garden Overview 🔍"
    st.subheader(title)
    for i in range(0, len(garden), 3):
        cols = st.columns(3)
        for j, plant in enumerate(garden[i : i+3]):
            with cols[j]:
                st.image(plant["image_bytes"], width=150)
                st.caption(f"{plant['name']} – {plant['type']}")

    week_start = st.session_state.week_start
    # 2) Weekly rainfall + nav buttons

    st.subheader("Weekly Rainfall Forecast 🌧️")
    
    # B) Two columns: Prev button | Next button
    col1, col2 = st.columns([1, 3])

    with col1:
        if st.button("← Previous Week", key="prev_week"):
            st.session_state.week_start -= datetime.timedelta(days=7)

    with col2:
        if st.button("Next Week →", key="next_week"):
            st.session_state.week_start += datetime.timedelta(days=7)
            
    week_start = st.session_state.week_start
    
    # Week label
    wk_start = st.session_state.week_start
    wk_end   = wk_start + datetime.timedelta(days=6)
    st.markdown(
        f"<div style='text-align:center; font-weight:bold;'>"
        f"Week of {wk_start.strftime('%B')} {wk_start.day} – "
        f"{wk_end.strftime('%B')} {wk_end.day}, {wk_end.year}"
        f"</div>",
        unsafe_allow_html=True,)

    # 1) make sure we have a persistent counters list
    if "plant_counters" not in st.session_state:
        st.session_state.plant_counters = [0] * len(st.session_state.garden)

    # 2) fetch rainfall
    try:
        weekly_rain = get_weekly_rainfall(st.session_state.week_start, lat, lon)
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        weekly_rain = [0.0] * 7

    # 3) compute watering schedule & updated counters
    schedule_df, new_counters = get_watering_schedule(
        st.session_state.garden,
        weekly_rain,
        st.session_state.week_start,
        st.session_state.plant_counters
    )

    # 4) persist those counters for next time
    st.session_state.plant_counters = new_counters

    # 5) Chart
    days_order = schedule_df["Day"].tolist()
    chart = (
        alt.Chart(schedule_df)
          .mark_bar()
          .encode(
              x=alt.X("Day", sort=days_order, title="Day"),
              y=alt.Y("Rain (mm)", title="Rain (mm)"),
          )
    )
    st.altair_chart(chart, use_container_width=True)

    # 6) Table
    st.subheader("Weekly Watering Schedule 📅")
    st.table(schedule_df)

else:
    st.info("📷 Please add at least one plant to your garden above.")
