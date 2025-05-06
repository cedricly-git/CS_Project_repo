import streamlit as st
import datetime
import pandas as pd

# Import helper modules
from plant_api import classify_plant_image
from weather_api import get_weekly_rainfall
from calendar_api import get_watering_advice

# --- Config and Session State Initialization ---
st.set_page_config(page_title="Plant Watering Assistant", layout="centered")
# Initialize session state for stored plant info and week navigation
if 'plant_info' not in st.session_state:
    st.session_state.plant_info = None
if 'week_start' not in st.session_state:
    # Align week_start to the Monday of the current week for a consistent calendar view
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())  # Monday of this week
    st.session_state.week_start = monday

# --- Title and Description ---
st.title("🌱 Plant Watering Assistant")
st.write("Upload a plant image to classify its type, then view a weekly calendar with rainfall data and watering reminders. "
         "All information is session-based (no login or database).")

# --- Plant Image Upload and Classification ---
with st.form("plant_form"):
    plant_name = st.text_input("Plant Nickname", help="Give your plant a name for easy reference.")
    image_file = st.file_uploader("Upload a picture of your plant", type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("Identify Plant")
if submitted:
    if not plant_name or not image_file:
        st.error("Please provide both a plant name and an image.")
    else:
        # Read image file and classify plant type using ML model (placeholder logic)
        plant_type = classify_plant_image(image_file)
        # Store plant info in session (name and type)
        st.session_state.plant_info = {"name": plant_name, "type": plant_type}
        # Display the result to the user
        st.success(f"**{plant_name}** has been classified as **{plant_type}**.")
        # Show the uploaded image
        st.image(image_file, caption=f"{plant_name} ({plant_type})", use_column_width=True)

# Only proceed to show calendar if a plant has been identified
if st.session_state.plant_info:
    plant_name = st.session_state.plant_info["name"]
    plant_type = st.session_state.plant_info["type"]

    # --- Char Title ---
    st.subheader("Daily Rainfall (mm)")
    # — Chart + Navigation in one row —
    left, center, right = st.columns([1, 6, 1])

    with left:
        if st.button("← Previous Week"):
            st.session_state.week_start -= datetime.timedelta(days=7)

    with right:
        if st.button("Next Week →"):
            st.session_state.week_start += datetime.timedelta(days=7)

    with center:
        # Title for the chart
        st.subheader("Daily Rainfall (mm)")
        # Your bar chart goes here
        st.bar_chart(df_rain["Rain (mm)"], height=200)

        # --- Retrieve Weather Data (Rainfall) ---
        week_start_date = st.session_state.week_start
        # Call Meteomatics API (via our weather_api module) to get daily rainfall for the week
        try:
            daily_rain = get_weekly_rainfall(week_start_date)
        except Exception as e:
            st.error(f"Error fetching weather data: {e}")
            daily_rain = [0]*7  # fallback to zeros to allow app to continue

        # --- Determine Watering Advice ---
        # Compute watering recommendation for each day, based on plant type and rainfall
        watering_schedule = get_watering_advice(plant_type, daily_rain)

        # --- Display Results: Rainfall Chart and Table ---
        # 1. Bar chart for daily rainfall, preserving chronological order
        #  ────────────────────────────────────────────────────────────────
        # Build the date labels in order
        dates = [
            (week_start_date + datetime.timedelta(days=i)).strftime("%a %d %b")
            for i in range(7)
        ]
        df_rain = pd.DataFrame({
            "Date": dates,
            "Rain (mm)": daily_rain
        })
        # Tell pandas that Date is an ordered categorical axis
        df_rain["Date"] = pd.Categorical(df_rain["Date"],
                                        categories=dates,
                                        ordered=True)
        df_rain = df_rain.set_index("Date")
    

        # 2. Weekly calendar table with rainfall and watering recommendation
        st.subheader("Weekly Watering Schedule")
        calendar_data = {
            "Day": [(week_start_date + datetime.timedelta(days=i)).strftime("%A") for i in range(7)],
            "Date": [(week_start_date + datetime.timedelta(days=i)).strftime("%d %b %Y") for i in range(7)],
            "Rain (mm)": daily_rain,
            "Watering Advice": watering_schedule
        }
        calendar_df = pd.DataFrame(calendar_data)
        # Use a static table for clarity
        st.table(calendar_df)

        # Optional: additional note or legend for watering advice
        st.write("**Note:** 'Watering Advice' is based on plant type rules and recent rain. "
                "For example, a recommendation of 'Water' means no significant rain recently and your plant likely needs watering.")
else:
    st.info("📷 Please upload a plant image and click 'Identify Plant' to see the watering schedule.")