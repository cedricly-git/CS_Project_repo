# Weather Feature Extraction
# This module provides functions to fetch and process weather data from the Meteomatics API.
# It includes functions to geocode city names to latitude and longitude,
# app/weather_api.py

#Import necessary libraries
import requests
import datetime

# Constants for Meteomatics API authentication
METEO_USER = "universityofstgallen_yan_grace"   
METEO_PASS = "2XPaF66p7o"

# 0) a tiny free geocoder (no API key) for “city → lat, lon”
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

#Reference:
# https://api.meteomatics.com/doc/api/1.0/overview/
#The code in weather_api.py was developed by the author with reference to public API documentation for Open-Meteo and Meteomatics. 
#The structure for making HTTP requests and parsing JSON responses follows standard usage examples provided by these services.