# nothing app before add week navigation button again

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
if 'week_start' not in st.session_state:
    import datetime
    today  = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    st.session_state.week_start = monday

st.title("Welcome to Plantelligence")

# Input for garden name
garden_name = st.text_input("Name your garden:", key="garden_name")

# --- Image Upload & Classification Form ---
st.subheader("Add a Plant to Your Garden")

with st.form("add_plant_form", clear_on_submit=True):
    plant_name_input = st.text_input("Plant Name", key="plant_name_input")
    plant_file_input = st.file_uploader(
        "Upload Plant Image", type=["jpg","jpeg","png"], key="plant_file_input"
    )
    submitted = st.form_submit_button("Add Plant")

if submitted:
    if not plant_name_input or not plant_file_input:
        st.warning("Please provide both a plant name and an image.")
    else:
        # Read & classify
        image_bytes = plant_file_input.read()
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        plant_type = classify_plant_image(img)

        # Append to garden
        st.session_state.garden.append({
            "name": plant_name_input,
            "type": plant_type,
            "image_bytes": image_bytes
        })

        st.success(f"Added **{plant_type}** “{plant_name_input}” to your garden.")

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
    # … after you've unpacked plant_info …  
week_start = st.session_state.week_start

# 1) Fetch or refresh rainfall data for that week
if 'weekly_rain' not in st.session_state or st.session_state.week_start != week_start:
    try:
        st.session_state.weekly_rain = get_weekly_rainfall(week_start)
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        st.session_state.weekly_rain = [0.0] * 7

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