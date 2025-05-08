# app/calendar_api.py
from datetime import timedelta
import pandas as pd

SIGNIFICANT_RAIN_THRESHOLD = 10.0  # mm considered heavy rain


def get_watering_schedule(garden: list, weekly_rain: list, week_start_date) -> pd.DataFrame:
    """
    Compute a 7-day watering schedule for a list of plants given weekly rainfall.
    - garden: list of dicts, each with 'name' and 'type' for each plant.
    - weekly_rain: iterable of 7 rainfall values (mm).
    - week_start_date: starting date (Monday).
    Returns a DataFrame with columns Day, Date, Rain (mm), Watering Advice.
    """
    # Build base calendar
    dates = [(week_start_date + timedelta(days=i)) for i in range(7)]
    day_names = [d.strftime("%A") for d in dates]
    date_strs = [d.strftime("%d %b %Y") for d in dates]
    rain_vals = [float(r) for r in weekly_rain]

    # Prepare advice per plant per day
    # Use existing logic for single plant; adapt for multiple
    def plant_needs_watering(plant_type, recent_rain):
        # import single-plant logic
        from calendar_api import SIGNIFICANT_RAIN_THRESHOLD as THRESH
        # Determine max dry days by type
        if plant_type == "Succulent":
            max_dry = 14
        elif plant_type == "Grass":
            max_dry = 7
        elif plant_type in ["Flower", "Edible"]:
            max_dry = 3
        elif plant_type == "Tree":
            max_dry = 10
        # Decide watering
        if recent_rain >= THRESH:
            return False, 0
        return True, max_dry

    # Track days since heavy rain per plant
    plant_counters = [0] * len(garden)
    advice = []
    for day_idx in range(7):
        day_rain = rain_vals[day_idx]
        needs = []
        for i, plant in enumerate(garden):
            got_heavy = (day_rain >= SIGNIFICANT_RAIN_THRESHOLD)
            if got_heavy:
                plant_counters[i] = 0
            else:
                plant_counters[i] += 1
            # check if counter exceeds max_dry
            plant_type = plant['type']
            _, max_dry = plant_needs_watering(plant_type, day_rain)
            if plant_counters[i] > max_dry:
                needs.append(plant['name'])
                plant_counters[i] = 0
        if needs:
            advice.append("Water: " + ", ".join(needs))
        else:
            advice.append("No water needed")

    # Build DataFrame
    df = pd.DataFrame({
        "Day": day_names,
        "Date": date_strs,
        "Rain (mm)": rain_vals,
        "Watering Advice": advice
    })
    return df
