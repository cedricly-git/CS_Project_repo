import requests

API_KEY = "your_api_key"
CITY = "London"
url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

temperature = data["main"]["temp"]
humidity = data["main"]["humidity"]
print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
