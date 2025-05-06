# This module contains logic to determine watering reminders based on plant type and rainfall.

# Define what is considered a "significant" rain that can delay watering (in mm)
SIGNIFICANT_RAIN_THRESHOLD = 10.0  # e.g., 10mm or more is a heavy rain day [oai_citation:1‡meteomatics.com](https://www.meteomatics.com/en/api/available-parameters/yearly-accumulated-day-counts/#:~:text=This%20parameter%20returns%20the%20number,since%201st%20of%20January)

def get_watering_advice(plant_type: str, daily_rain: list) -> list:
    """
    Given a plant type and a list of 7 daily rainfall amounts (mm),
    return a list of 7 strings ("Water" or "No water needed") for each corresponding day.
    The logic is based on general watering rules for the plant category and recent rain.
    """
    advice_list = []
    days_since_significant_rain = 0  # counter for days since last heavy rain

    # Determine watering frequency needs based on plant type (in days without rain)
    if plant_type == "Cacti/Succulents":
        # Very infrequent watering; roughly every 14-21 days if no rain, and not if rain is forecast
        max_dry_days = 14
    elif plant_type == "Grasses/Lawns":
        # Need consistent moisture; water at least once a week if no significant rain
        max_dry_days = 7
    elif plant_type == "Flowering Plants":
        # Water a few times a week in hot weather if no rain for 3+ days
        max_dry_days = 3
    elif plant_type == "Fruiting Plants":
        # Regular watering during fruiting; don't need if heavy rain in last ~3 days
        max_dry_days = 3
    elif plant_type == "Trees/Shrubs":
        # Deep watering every 1-2 weeks if no rain
        max_dry_days = 10
    elif plant_type == "Ferns/Mosses":
        # Very frequent watering (prefer constantly moist); if no rain even for 2 days, water
        max_dry_days = 2
    else:
        # Default for unknown types
        max_dry_days = 7

    # Iterate through each day to decide watering
    for rain in daily_rain:
        # Check if it rained significantly this day
        if rain >= SIGNIFICANT_RAIN_THRESHOLD:
            days_since_significant_rain = 0  # reset counter if heavy rain occurred
            advice_list.append("No water needed")
        else:
            days_since_significant_rain += 1
            # If it's been more than max_dry_days without heavy rain, advise watering
            if days_since_significant_rain > max_dry_days:
                advice_list.append("Water")
                days_since_significant_rain = 0  # assume we water this day, reset dry counter
            else:
                advice_list.append("No water needed")

    return advice_list
