# --- Calendar Feature ---
# The following provides a function to compute a watering schedule for a garden based on weekly precipitation.
# Taken into account are the type of plants, their watering needs, and the amount of precipitation received.
from datetime import timedelta # to calculate future dates
import pandas as pd # for the creation of the table (DataFrame output)

# --- Reference ---
# https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
# This code was written by the author with reference to online examples and documentation, including Python and pandas resources. 
# Some logic patterns were adapted from community discussions (e.g., Stack Overflow) for educational purposes.
# https://docs.python.org/3/library/
# Used to understand and correctly apply Python's standard library modules, especially datetime.timedelta and enumerate().

# meteo swiss defines from on 10 mm of precipitation within 24 h as heavy precipitation, thus we have choosen 10 mm as a threshold as well
# https://www.meteoswiss.admin.ch/weather/weather-and-climate-from-a-to-z/precipitation.html
SIGNIFICANT_RAIN_THRESHOLD = 10.0  # mm above this value (i.e. 10mm) is considered sufficient to be sufficient to water the plants

# Function to compute watering schedule
# This function computes a 7-day watering schedule for a list of plants given weekly precipitation.
def get_watering_schedule(garden: list, weekly_rain: list, week_start_date, plant_counters: list) -> pd.DataFrame:
    """
    Compute a 7-day watering schedule for a list of plants given weekly rainfall.
    - garden: list of dicts, each with 'name' and 'type' for each plant.
    - weekly_rain: iterable of 7 rainfall values (mm).
    - week_start_date: starting date (Monday).
    - plant_counters: list tracking days since last significant rain for each plant.
    Returns a DataFrame with columns Day, Date, Rain (mm), Watering Advice, and updated plant_counters.
    """
    # source: ChatGPT assisted in the creation of the function concept and implementation. 
    # Build base calendar
    # generates a list of dates objects for each day of the week starting from the starting date
    dates = [(week_start_date + timedelta(days=i)) for i in range(7)]
    # conversion of the date objects to their respective weekday names (i.e. Monday, Tuesday, etc.)
    day_names = [d.strftime("%A") for d in dates]
    # conversion of respective date objects to date strings (e.g. 12 June 2025)
    date_strs = [d.strftime("%d %b %Y") for d in dates]
    # makes sure that all precipitation values are floats in mm
    rain_vals = [float(r) for r in weekly_rain]

    # Prepare advice per plant per day; determines which, if any, of the plants need watering
    # sources for the choosed maximum number of drr days, i.e. days without precipitation each plant can go: 
    # amount of days recommended is based on maximum number and including a margin of safety (i.e. the recommended days are shorter than the maximum amount the plant could techincally survive)
    # https://harddy.com/blogs/succulents-cacti-faq/how-long-can-succulents-survive-without-water#:~:text=Outdoor%20Hot%20Climates,to%20sustain%20them%20year%2Dround.
    # https://extension.missouri.edu/publications/g6722#:~:text=Most%20grasses%20will%20survive%204%20to%206,as%20soon%20as%20possible%20after%20water%20recedes.
    # https://foodgardening.mequoda.com/daily/watering-irrigation/how-often-should-i-water-my-plants-in-the-summer/#:~:text=Most%20plants%20will%20grow%20deeper,or%20three%20days%20this%20way.
    # https://tuigarden.co.nz/inspiration-hub/ideas-and-inspiration/water-saving-guide/
    # https://woodlandswater.org/nurturing-mature-trees-through-drought-a-guide-to-proper-watering/#:~:text=Deep%2C%20Infrequent%20Watering:%20Just%20like,a%20longer%20period%20of%20time.
    def plant_needs_watering(plant_type, recent_rain):
        # Determine max dry days by type before the respective plant needs watering
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
        # If recent rain is significant enough (enough amount of water), irrespective of the number of dry days, watering is not required
        if recent_rain >= SIGNIFICANT_RAIN_THRESHOLD:
            return False, 0 # no watering needed and no concern for dry days today
        return True, max_dry # in all other cases, use the maximum amount of dry days value for comparison later on

    # list to track and store days since last significant rain per plant and watering advice
    advice = []
    updated_counters = plant_counters[:]  # Create a copy of the counters to update

    # source: ChatGPT assisted in the creation of the function concept and implementation. 
    # iterate for each day of the week (day 0 to day 6)
    for day_idx in range(7):
        day_rain = rain_vals[day_idx] # gets amount of precipitation of current day
        needs = [] # list for plant names that require watering today
        
        # checking of watering requirement of each indiviudal plant
        for i, plant in enumerate(garden):
            got_heavy = (day_rain >= SIGNIFICANT_RAIN_THRESHOLD) # checking if today's precipitation is significiant/sufficient
            
            # if sufficient precipitation occured that day, reset the plant's counter
            if got_heavy:
                updated_counters[i] = 0
            else:
                updated_counters[i] += 1  # increment the dry day counter for this plant
            
            plant_type = plant['type']
            _, max_dry = plant_needs_watering(plant_type, day_rain) # determine whether the plant potentially requires watering and retrieve maximum number of allowed dry days
            
            # Check if the plant needs watering based on the max dry period; if the dry period exceeds the maxmium, the plant requires watering
            if updated_counters[i] > max_dry:
                needs.append(plant['name']) # addition of plant to today's watering list
                updated_counters[i] = 0  # Reset the counter after watering # resetting of the counter after watering completed

        # build the advice string for each day
        if needs:
            advice.append("Water: " + ", ".join(needs)) # recommendation of watering specific plants
        else:
            advice.append("No water needed") # none of the plants require watering that day

    # building of DataFrame to display watering scedule in form of table
    # creation of a DataFrame with the computed watering schedule
    df = pd.DataFrame({
        "Day": day_names,
        "Date": date_strs,
        "Rain (mm)": rain_vals,
        "Watering Advice": advice
    })
    # return both the schedule DataFrame and the updated counters to use during the next cycle
    return df, updated_counters




