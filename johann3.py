# plant_id_with_image.py

import requests
import base64

# 🔐 Insert your actual API key here
API_KEY = "insert your API key"
API_URL = "https://api.plant.id/v2/identify"

# 📸 Path to a local image of a plant
IMAGE_PATH = "plant.jpg"  # <-- replace with your image filename

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
print("Response Text:\n", response.text)