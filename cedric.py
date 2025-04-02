import requests
import pandas as pd

API_KEY = "1AhbgX6f-AVV6SPFX7-1q9v0HJ55kghAcuz3XE_4cms"
url = "https://trefle.io/api/v1/plants"  # Adjust with correct endpoint

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    # Inspect the structure of the response first
    print(data)
    
    # Assuming 'data' key holds the actual plant data, create a DataFrame from it
    df = pd.DataFrame(data.get('data', []))  # Default to an empty list if 'data' key doesn't exist
    print(df.head())
else:
    print(f"Failed to fetch data: {response.status_code}")
