from datetime import timedelta
import pandas as pd

SIGNIFICANT_RAIN_THRESHOLD = 10.0  # mm considered sufficient rain to water the plants

def get_watering_schedule(garden: list, weekly_rain: list, week_start_date, plant_counters: list) -> pd.DataFrame:
    """
    Compute a 7-day watering schedule for a list of plants given weekly rainfall.
    - garden: list of dicts, each with 'name' and 'type' for each plant.
    - weekly_rain: iterable of 7 rainfall values (mm).
    - week_start_date: starting date (Monday).
    - plant_counters: list tracking days since last significant rain for each plant.
    Returns a DataFrame with columns Day, Date, Rain (mm), Watering Advice, and updated plant_counters.
    """
    # Build base calendar
    dates = [(week_start_date + timedelta(days=i)) for i in range(7)]
    day_names = [d.strftime("%A") for d in dates]
    date_strs = [d.strftime("%d %b %Y") for d in dates]
    rain_vals = [float(r) for r in weekly_rain]

    # Prepare advice per plant per day
    def plant_needs_watering(plant_type, recent_rain):
        # Determine max dry days by type
        if plant_type == "Succulent":
            max_dry = 14
        elif plant_type == "Grass":
            max_dry = 6
        elif plant_type == "Flower":
            max_dry = 2
        elif plant_type == "Edible":
            max_dry = 4
        elif plant_type == "Tree":
            max_dry = 9
        # If recent rain is significant, don't water
        if recent_rain >= SIGNIFICANT_RAIN_THRESHOLD:
            return False, 0
        return True, max_dry

    # Track days since last significant rain per plant
    advice = []
    updated_counters = plant_counters[:]  # Create a copy of the counters to update
    
    for day_idx in range(7):
        day_rain = rain_vals[day_idx]
        needs = []
        
        for i, plant in enumerate(garden):
            got_heavy = (day_rain >= SIGNIFICANT_RAIN_THRESHOLD)
            
            # If heavy rain occurs, reset the plant's counter
            if got_heavy:
                updated_counters[i] = 0
            else:
                updated_counters[i] += 1  # Increment the day counter for this plant
            
            plant_type = plant['type']
            _, max_dry = plant_needs_watering(plant_type, day_rain)
            
            # Check if the plant needs watering based on the max dry period
            if updated_counters[i] > max_dry:
                needs.append(plant['name'])
                updated_counters[i] = 0  # Reset the counter after watering
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
    return df, updated_counters
