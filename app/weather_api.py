import requests
import datetime

# Configuration: Meteomatics API credentials (to be provided by user)
METEO_USER = "universityofstgallen_soerensen_johann"   
METEO_PASS = "iDV83e4R6e"

# Define a default location for weather data (latitude, longitude)
# Here we use St. Gallen, Switzerland as an example location
DEFAULT_LAT = 47.4245
DEFAULT_LON = 9.3767

def get_weekly_rainfall(week_start_date: datetime.date, lat: float = DEFAULT_LAT, lon: float = DEFAULT_LON) -> list:
    """
    Fetch daily rainfall (in mm) for 7 days starting from week_start_date (inclusive) at the given location.
    Returns a list of 7 rainfall values (mm) for each day.
    """
    # Construct the Meteomatics API URL for daily precipitation (24h accumulated) 
    # from week_start_date to week_start_date+7 days (which gives 7 values, one per day).
    # Format dates to ISO 8601 with UTC time (00:00Z for daily accumulated precipitation).
    start_dt = datetime.datetime.combine(week_start_date, datetime.time.min).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date = week_start_date + datetime.timedelta(days=7)  # 7 days later (exclusive end)
    end_dt = datetime.datetime.combine(end_date, datetime.time.min).strftime("%Y-%m-%dT%H:%M:%SZ")
    # Parameter for daily precipitation is "precip_24h:mm"
    url = f"https://api.meteomatics.com/{start_dt}--{end_dt}:P1D/precip_24h:mm/{lat},{lon}/json"

    # Perform API request with basic authentication
    response = requests.get(url, auth=(METEO_USER, METEO_PASS))
    if response.status_code != 200:
        raise Exception(f"Meteomatics API error: {response.status_code} {response.text}")

    data = response.json()
    # Parse JSON to extract the list of daily precipitation values
    try:
        dates_data = data["data"][0]["coordinates"][0]["dates"]
        rain_values = [entry.get("value", 0) for entry in dates_data]
        # The API returns 8 values if we include the end date; take first 7 entries for the week
        daily_rain = rain_values[:7]
    except (KeyError, IndexError) as e:
        raise Exception("Unexpected response format from Meteomatics API") from e

    return daily_rain
