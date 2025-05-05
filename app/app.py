# app/app.py

import streamlit as st
import datetime
import pandas as pd

# Import our helper modules
from plant_api import classify_plant_image
from weather_api import get_weekly_rainfall
from calendar_api import get_watering_advice

# --- Config & Session State ---
st.set_page_config(page_title="Plant Watering Assistant", layout="centered")

if 'plant_info' not in st.session_state:
    st.session_state.plant_info = None

if 'week_start' not in st.session_state:
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())  # get this week's Monday
    st.session_state.week_start = monday

# --- Title & Instructions ---
st.title("🌱 Plant Watering Assistant")
st.write(
    "Upload a plant image to classify its type, then view a weekly calendar with "
    "rainfall data and watering reminders. (All data is session-based; no login required.)"
)

# --- Image Upload & Classification Form ---
with st.form("plant_form"):
    plant_name = st.text_input("Plant Nickname", help="Give your plant a name for easy reference.")
    image_file = st.file_uploader("Upload a picture of your plant", type=["png","jpg","jpeg"])
    submitted = st.form_submit_button("Identify Plant")

if submitted:
    if not plant_name or not image_file:
        st.error("Please provide both a plant name and an image.")
    else:
        plant_type = classify_plant_image(image_file)
        st.session_state.plant_info = {"name": plant_name, "type": plant_type}
        st.success(f"**{plant_name}** has been classified as **{plant_type}**.")
        st.image(image_file, caption=f"{plant_name} ({plant_type})", use_column_width=True)

# --- Main Calendar & Chart View ---
if st.session_state.plant_info:
    plant_name = st.session_state.plant_info["name"]
    plant_type = st.session_state.plant_info["type"]
    week_start = st.session_state.week_start

    # 1) Fetch rainfall data
    try:
        daily_rain = get_weekly_rainfall(week_start)
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        daily_rain = [0]*7

    # 2) Build the bar chart data (Mon→Sun)
    dates = [
        (week_start + datetime.timedelta(days=i)).strftime("%a %d %b")
        for i in range(7)
    ]
    df_rain = pd.DataFrame({
        "Date": dates,
        "Rain (mm)": daily_rain
    })
    # Preserve the order explicitly
    df_rain["Date"] = pd.Categorical(df_rain["Date"], categories=dates, ordered=True)
    df_rain = df_rain.set_index("Date")

    # 3) Navigation + Chart
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← Previous Week"):
            st.session_state.week_start -= datetime.timedelta(days=7)
            st.experimental_rerun()
    with col3:
        if st.button("Next Week →"):
            st.session_state.week_start += datetime.timedelta(days=7)
            st.experimental_rerun()
    with col2:
        st.subheader("Daily Rainfall (mm)")
        st.bar_chart(df_rain["Rain (mm)"], height=200)

    # 4) Watering Advice Table
    watering_schedule = get_watering_advice(plant_type, daily_rain)
    st.subheader("Weekly Watering Schedule")
    calendar_data = {
        "Day": [(week_start + datetime.timedelta(days=i)).strftime("%A") for i in range(7)],
        "Date": [(week_start + datetime.timedelta(days=i)).strftime("%d %b %Y") for i in range(7)],
        "Rain (mm)": daily_rain,
        "Watering Advice": watering_schedule
    }
    calendar_df = pd.DataFrame(calendar_data)
    st.table(calendar_df)

else:
    st.info("📷 Please upload a plant image and click 'Identify Plant' to see the watering schedule.")
    
