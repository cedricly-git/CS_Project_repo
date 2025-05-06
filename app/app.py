# app/app.py
import streamlit as st
from weather_api import get_weekly_rainfall
from copy_plant_api_test import classify_plant_image
from calendar_api import get_watering_schedule
from PIL import Image
from io import BytesIO
import altair as alt

# Initialize session state for garden
if 'garden' not in st.session_state:
    st.session_state.garden = []

st.title("Welcome to Plantelligence")

# Input for garden name
garden_name = st.text_input("Name your garden:", key="garden_name")

# Section to add a new plant to the garden
st.subheader("Add a Plant to Your Garden")
plant_name = st.text_input("Plant Name", key="plant_name")
plant_image_file = st.file_uploader("Upload Plant Image", type=["jpg", "jpeg", "png"], key="plant_image")

if st.button("Add Plant"):
    if plant_name and plant_image_file:
        # Read and classify the uploaded plant image
        image_bytes = plant_image_file.read()
        img = Image.open(BytesIO(image_bytes))
        img = img.convert("RGB")  # ensure compatibility for classification
        plant_type = classify_plant_image(img)
        # Store the plant's info in the session state garden list
        st.session_state.garden.append({
            "name": plant_name,
            "type": plant_type,
            "image_bytes": image_bytes
        })
        # Clear input fields for the next entry
        st.session_state.plant_name = ""
        st.session_state.plant_image = None
        st.success(f"Added {plant_name} ({plant_type}) to garden.")
    else:
        st.warning("Please provide both a plant name and an image.")

# If there are plants in the garden, display the overview, rainfall chart, and watering schedule
if st.session_state.garden:
    # Garden overview with all plants
    st.subheader(f"Garden Overview{': ' + garden_name if garden_name else ''}")
    # Display all plants in a gallery (thumbnails with name and type)
    garden = st.session_state.garden
    for i in range(0, len(garden), 3):
        cols = st.columns(min(3, len(garden) - i))
        for j, plant in enumerate(garden[i:i+3]):
            with cols[j]:
                st.image(plant["image_bytes"], width=150, caption=f"{plant['name']} - {plant['type']}")
    # Fetch weekly rainfall data (once) for the garden's location (if applicable)
    if 'weekly_rain' not in st.session_state:
        st.session_state.weekly_rain = get_weekly_rainfall()
    weekly_rain = st.session_state.weekly_rain

    # Display the weekly rainfall chart
    st.subheader("Weekly Rainfall Forecast")
    # Get watering schedule (which also computes day labels and uses rainfall data)
    schedule_df = get_watering_schedule(st.session_state.garden, weekly_rain)
    # Prepare data for chart (avoid special characters in column names for Altair)
    chart_df = schedule_df[["Day", "Rain (mm)"]].copy()
    chart_df.rename(columns={"Rain (mm)": "Rain_mm"}, inplace=True)
    days_order = chart_df["Day"].tolist()
    chart = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X('Day:N', sort=days_order, title='Day'),
        y=alt.Y('Rain_mm:Q', title='Rain (mm)')
    )
    st.altair_chart(chart, use_container_width=True)

    # Display the consolidated watering advice table
    st.subheader("Weekly Watering Schedule")
    st.table(schedule_df.to_dict(orient='records'))