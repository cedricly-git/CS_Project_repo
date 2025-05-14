# --- Weather Feature Extraction ---
# This module provides functions to fetch and process weather data from the Meteomatics API.
# It includes functions to geocode city names to latitude and longitude, and to retrieve weekly rainfall data for a given location.
# We use the output of this feature in "app.py" to have access to the weather data for the selected city.
# The data is used for watering recommendations.

# --- Reference ---
# https://api.meteomatics.com/doc/api/1.0/overview/
# https://requests.readthedocs.io/en/latest/user/authentication/
# The code in weather_api.py was developed by the author with reference to public API documentation for Open-Meteo and Meteomatics. 
# The structure for making HTTP requests and parsing JSON responses follows standard usage examples provided by these services.

# Import necessary libraries
# Requests is used for making HTTP requests to the Meteomatics API.
# Datetime is used for handling date and time operations.
import requests
import datetime

# Constants for Meteomatics API authentication
# Set the username and password for the Meteomatics API
METEO_USER = "universityofstgallen_yan_grace"   
METEO_PASS = "2XPaF66p7o"

# Function to geocode city names to latitude and longitude
# This function uses the Open-Meteo geocoding API to convert a city name into its corresponding latitude and longitude.
# And returns a tuple of (latitude, longitude).
def geocode(city: str) -> tuple[float, float]:
    """Use Open-Meteo’s geocoding to turn a city name into (lat, lon)."""
    resp = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1}
    )
    resp.raise_for_status()
    results = resp.json().get("results")
    if not results:
        # fallback to St Gallen if nothing found
        return 47.4245, 9.3767
    best = results[0]
    return float(best["latitude"]), float(best["longitude"])

# Use the latitude and longitude to get the weekly rainfall data
# This function fetches daily rainfall data for a week starting from a given date.
def get_weekly_rainfall(week_start_date: datetime.date, lat: float, lon: float) -> list:
    """Fetch daily rainfall (in mm) for 7 days starting from week_start_date (inclusive) at the given location.
    Returns a list of 7 rainfall values (mm) for each day."""
    # Construct the Meteomatics API URL for daily precipitation (24h accumulated) 
    # from week_start_date to week_start_date+7 days (which gives 7 values, one per day).
    # Format dates to ISO 8601 with UTC time (00:00Z for daily accumulated precipitation).
    start_dt = datetime.datetime.combine(week_start_date, datetime.time.min).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date = week_start_date + datetime.timedelta(days=7)  # 7 days later (exclusive end)
    end_dt = datetime.datetime.combine(end_date, datetime.time.min).strftime("%Y-%m-%dT%H:%M:%SZ")
    # Parameter for daily precipitation is "precip_24h:mm"
    url = f"https://api.meteomatics.com/{start_dt}--{end_dt}:P1D/precip_24h:mm/{lat},{lon}/json"

    # Perform API request with basic authentication
    # The API requires authentication using a username and password.
    # The username and password are passed in the request using the auth parameter.
    response = requests.get(url, auth=(METEO_USER, METEO_PASS))
    if response.status_code != 200:
        raise Exception(f"Meteomatics API error: {response.status_code} {response.text}")

    data = response.json()
    # Parse JSON to extract the list of daily precipitation values

    # The response structure is nested, so we need to navigate through the JSON to find the relevant data.
    try:
        dates_data = data["data"][0]["coordinates"][0]["dates"]
        rain_values = [entry.get("value", 0) for entry in dates_data]
        # The API returns 8 values if we include the end date; take first 7 entries for the week
        daily_rain = rain_values[:7]
    except (KeyError, IndexError) as e:
        raise Exception("Unexpected response format from Meteomatics API") from e

    # return the list of daily rainfall values
    return daily_rain