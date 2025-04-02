import requests
import pandas as pd

url = "https://api.example.com/data"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)  # Convert JSON to DataFrame
    print(df.head())
else:
    print(f"Failed to fetch data: {response.status_code}")
