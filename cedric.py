import requests
import pandas as pd

API_KEY = "1AhbgX6f-AVV6SPFX7-1q9v0HJ55kghAcuz3XE_4cms"
url = "https://api.example.com/data"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    print(df.head())
else:
    print(f"Failed to fetch data: {response.status_code}")
