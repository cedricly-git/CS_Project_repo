# plant_id_with_image.py

import requests
import base64
import json

# 🔐 Insert your actual API key here
API_KEY = "BjJAbPigzeN2PU1bmHvVWfbBcJBpcakBMNCKBiq9lIFfxO0So3"
API_URL = "https://api.plant.id/v2/identify"

# 📸 Path to a local image of a plant
IMAGE_PATH = "/Users/johannsorensen/Desktop/plant.jpg"

# 🔁 Convert image to base64 string
with open(IMAGE_PATH, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# 📦 Payload with actual image
payload = {
    "api_key": API_KEY,
    "images": [encoded_image],
    "organs": ["leaf"],
    "similar_images": True,
    "plant_language": "en",
    "plant_details": ["common_names", "url", "name_authority"]
}

# 🚀 Send the POST request
response = requests.post(API_URL, json=payload)

# 🧾 Print status and result
print("Status Code:", response.status_code)
# Parse and print top plant prediction
response_data = response.json()

# Check if suggestions are available
if "suggestions" in response_data and response_data["suggestions"]:
    top_match = response_data["suggestions"][0]
    plant_name = top_match["plant_name"]
    probability = top_match["probability"]
    common_names = top_match.get("plant_details", {}).get("common_names", [])

    print("🌿 Top Match:")
    print(f"Scientific Name: {plant_name}")
    print(f"Common Names: {', '.join(common_names) if common_names else 'N/A'}")
    print(f"Confidence: {round(probability * 100, 2)}%")
else:
    print("No plant suggestions found.")

    flow = InstalledAppFlow.from_credentials.json('credentials.json', SCOPES)
    
