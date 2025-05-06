# app/app.py

import streamlit as st
import datetime
from datetime import timedelta
from io import BytesIO
from PIL import Image
import altair as alt

from plant_api import classify_plant_image
from weather_api import get_weekly_rainfall
from calendar_api import get_watering_schedule

# --- Page config & session-state init ---
st.set_page_config(page_title="Plantelligence", layout="centered")

if 'garden' not in st.session_state:
    st.session_state.garden = []

if 'week_start' not in st.session_state:
    today = datetime.date.today()
    monday = today - timedelta(days=today.weekday())
    st.session_state.week_start = monday

# --- Title & garden-name input ---
st.title("Welcome to Plantelligence")
garden_name = st.text_input("Name your garden:", key="garden_name")

# --- Add-plant form ---
st.subheader("Add a Plant to Your Garden")
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
        # read bytes once
        image_bytes = plant_file.read()
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        plant_type = classify_plant_image(img)
        st.session_state.garden.append({
            "name": plant_name,
            "type": plant_type,
            "image_bytes": image_bytes
        })
        st.success(f"Added **{plant_type}** “{plant_name}” to your garden.")

# --- If we have at least one plant, show overview + charts ---
if st.session_state.garden:
    garden = st.session_state.garden

    # 1) Garden overview gallery
    title = f"Garden Overview: {garden_name}" if garden_name else "Garden Overview"
    st.subheader(title)
    for i in range(0, len(garden), 3):
        cols = st.columns(3)
        for j, plant in enumerate(garden[i : i+3]):
            with cols[j]:
                st.image(plant["image_bytes"], width=150)
                st.caption(f"{plant['name']} – {plant['type']}")

    # 2) Weekly rainfall + nav buttons
    week_start = st.session_state.week_start

    st.subheader("Weekly Rainfall Forecast")
    prev_col, next_col = st.columns(2)
    with prev_col:
        if st.button("← Previous Week"):
            st.session_state.week_start -= timedelta(days=7)
            st.experimental_rerun()
    with next_col:
        if st.button("Next Week →"):
            st.session_state.week_start += timedelta(days=7)
            st.experimental_rerun()

    # 3) Fetch rainfall
    try:
        weekly_rain = get_weekly_rainfall(week_start)
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        weekly_rain = [0.0]*7

    # 4) Compute consolidated watering schedule
    schedule_df = get_watering_schedule(garden, weekly_rain)

    # 5) Chart
    days_order = schedule_df["Day"].tolist()
    chart = (
        alt.Chart(schedule_df)
        .mark_bar()
        .encode(
            x=alt.X("Day", sort=days_order, title="Day"),
            y=alt.Y("Rain (mm)", title="Rain (mm)")
        )
    )
    st.altair_chart(chart, use_container_width=True)

    # 6) Table
    st.subheader("Weekly Watering Schedule")
    st.table(schedule_df)

else:
    st.info("📷 Please add at least one plant to your garden above.")