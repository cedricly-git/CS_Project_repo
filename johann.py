#installing the HTTP
import requests

# Your Trefle API key
API_KEY = "1AhbgX6f-AVV6SPFX7-1q9v0HJ55kghAcuz3XE_4cms"

# Base URL for Trefle API
BASE_URL = "https://trefle.io/api/v1/"

def get_plant_details(plant_name):
    try:
        # Make a request to search for a plant by name
        response = requests.get(
            f"{BASE_URL}plants/search",
            params={"q": plant_name, "token": API_KEY}
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            if data['data']:
                for plant in data['data']:
                    print(f"Name: {plant['common_name']} ({plant['scientific_name']})")
                    print(f"Family: {plant['family']}")
                    print(f"Genus: {plant['genus']}")
                    print(f"Image: {plant.get('image_url', 'No image available')}")
                    print("-" * 50)
                    print(response.status_code)
                    print(response.text) 
            else:
                print("No plants found with that name.")
        else:
            print("Error:", response.status_code, response.json())
           
    except Exception as e:
        print("An error occurred:", str(e))

# Example usage
get_plant_details("rose")
