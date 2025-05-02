# weather API
import requests

# API keys inserted
API_key
API_URL

# function to get weather data for given city 
def get_weather(city, api_key): 
  base_url = 
  params = {
    'q': city,             # q is city name one wants data for
    'appid': api_key,      # personal API key
    'units': 'metric'      # For temperature units in celcius
  }

# sends GET request to weather API with parameters
reponse = request.get(base_url, params=params)

# check is response was successful (status code 200)
if response.status_code == 200:
  # conversion into Python dictionary
  data = resonse.json()

  weather = {
    'city': data['name'],
    'temperature': data['main', 'temp'],
    'description': data['weather'][0]['description'],
    'humidity': data['main', 'humnidity']
  }

  # extract useful information from repsonse 
  return weather
  # error message
else: 
  print("Error:", response.status_code)
  return none



  
