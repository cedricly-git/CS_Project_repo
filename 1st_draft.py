import requests

API_KEY = ""
CITY = "St. Gallen"
url = f"https://plant.id/api/v3"

response = requests.get(url)
data = response.json()

temperature = data["main"]["temp"]
humidity = data["main"]["humidity"]
print(f"Temperature: {temperature}°C, Humidity: {humidity}%")

if temperature > 30 and humidity < 40:
    print("Water your plant! It's hot and dry.")
elif data["weather"][0]["main"] == "Rain":
    print("No need to water. It rained recently.")
else:
    print("Your plant is fine for now.")
