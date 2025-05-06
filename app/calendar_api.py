# calendar_api

from datetime import datetime, timedelta
import pandas as pd

def get_watering_schedule(garden, weekly_rain):
    """
    Compute a 7-day watering schedule for a list of plants given weekly rainfall.
    - garden: list of dicts, each with 'name' and 'type' keys for each plant.
    - weekly_rain: iterable of 7 rainfall values (in mm) for the next 7 days.
    Returns a pandas DataFrame with columns: Day, Date, Rain (mm), Watering Advice.
    """
    # If no plants provided, return an empty schedule
    if not garden:
        columns = ["Day", "Date", "Rain (mm)", "Watering Advice"]
        return pd.DataFrame(columns=columns)

    # Ensure we have exactly 7 days of rainfall data
    try:
        rain_list = list(weekly_rain)
    except Exception as e:
        raise ValueError("weekly_rain must be an iterable of length 7") from e
    if len(rain_list) < 7:
        # Pad with 0 mm if data is missing
        rain_list = (rain_list + [0.0] * 7)[:7]
    elif len(rain_list) > 7:
        rain_list = rain_list[:7]
    rains = [float(r) for r in rain_list]

    def plant_needs_water(plant_type, rain_amount):
        """Determine if a plant of given type needs watering given the rain amount."""
        pt = plant_type.lower()
        # Default threshold (mm of rain) above which watering is not needed
        threshold = 3.0
        # Adjust threshold based on plant type (placeholder logic per plant water needs)
        if "cactus" in pt or "succulent" in pt:
            threshold = 1.0   # low water requirement
        elif "fern" in pt or "moss" in pt:
            threshold = 5.0   # high water requirement
        elif "orchid" in pt or "lily" in pt or "hydrangea" in pt or "ivy" in pt:
            threshold = 4.0   # moderate-high water requirement
        elif "rose" in pt or "herb" in pt or "flower" in pt:
            threshold = 3.0   # moderate water requirement (default)
        # Needs watering if rain is below the threshold
        return rain_amount < threshold

    # Build the schedule for each day
    schedule = []
    today = datetime.today()
    for i, rain in enumerate(rains):
        day_date = today + timedelta(days=i)
        day_name = day_date.strftime("%a")       # e.g. Mon, Tue
        date_str = day_date.strftime("%b %d")    # e.g. Jan 05
        # Determine which plants require watering on this day
        plants_to_water = [plant["name"] for plant in garden if plant_needs_water(plant["type"], rain)]
        if plants_to_water:
            advice = ", ".join(f"Water {name}" for name in plants_to_water)
        else:
            advice = "No watering needed"
        schedule.append({
            "Day": day_name,
            "Date": date_str,
            "Rain (mm)": round(rain, 1),
            "Watering Advice": advice
        })

    # Convert the schedule list to a DataFrame for easy display
    return pd.DataFrame(schedule)
