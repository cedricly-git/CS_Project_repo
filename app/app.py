# app/app.py

#LINE 7 FUNCTION CLASSIFY_PLANT_IMAGE FROM PLANT_API.PY NOT COPY

import streamlit as st
from weather_api import get_weekly_rainfall
from plant_api import classify_plant_image
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

# --- Image Upload & Classification Form ---
st.subheader("Add a Plant to Your Garden")

# Step A: the two inputs, each with its own key
plant_name_input  = st.text_input("Plant Name", key="plant_name_input")
plant_file_input  = st.file_uploader(
    "Upload Plant Image",
    type=["jpg", "jpeg", "png"],
    key="plant_file_input"
)

# Step B: callback that runs when you click "Add Plant"
def add_plant_to_garden():
    # read and classify
    image_bytes = st.session_state.plant_file_input.read()
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    plant_type = classify_plant_image(img)

    # append to your garden list
    st.session_state.garden.append({
        "name":  st.session_state.plant_name_input,
        "type":  plant_type,
        "image_bytes": image_bytes
    })

    # clear the inputs for the next entry
    st.session_state.plant_name_input = ""
    st.session_state.plant_file_input = None
    st.success(f"Added **{plant_type}** “{st.session_state.plant_name_input}” to your garden.")

# Step C: the button wired to that callback
st.button("Add Plant", on_click=add_plant_to_garden)
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