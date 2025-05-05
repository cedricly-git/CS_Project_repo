import requests
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Authentication of Google Calendar

SCOPES = ['https://www.googleapis.com/auth/calendar']

def google_calendar_service():
    """
    Authenticates with Google Calendar API and returns a service object.
    """
    creds = None

    # Load existing token if available
    if creds := Credentials.from_authorized_user_file('token.json', SCOPES):
        pass
    else:
        # If no token or token expired, authenticate via browser
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        # Save token for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

# Fetch Data from Weather API

def get_precipitation_data(username, password, location):
    """
    Retrieves daily precipitation forecast from Meteomatics API for given coordinates.
    """
    today = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    future = (datetime.datetime.utcnow() + datetime.timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Get Access Token
    auth = requests.get(
        'https://login.meteomatics.com/api/v1/token',
        headers={"Authorization": f"Basic {requests.auth._basic_auth_str(username, password)}"}
    )

    if auth.status_code != 200:
        print("Failed to authenticate with Meteomatics.")
        return []

    token = auth.json()['access_token']

    # Precipitation Data Requested
    lat, lon = location
    parameter = "precip_24h:mm"
    url = f"https://api.meteomatics.com/{today}--{future}:P1D/{parameter}/{lat},{lon}/json?access_token={token}"

    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to get weather data.")
        return []

    data = response.json()
    dates = data['data'][0]['coordinates'][0]['dates']
    return [(d['date'], d['value']) for d in dates]

# Creation of Calendar Event
def create_weather_events(service, data):
    """
    Creates daily Google Calendar events with precipitation values.
    """
    for date_str, value in data:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").date()
        event = {
            'summary': f'Rain Forecast: {value:.1f} mm',
            'description': f'Daily precipitation forecast for St. Gallen: {value:.1f} mm',
            'start': {'date': date.isoformat()},
            'end': {'date': (date + datetime.timedelta(days=1)).isoformat()},
        }
        service.events().insert(calendarId='primary', body=event).execute()
        print(f"Added event for {date}: {value:.1f} mm")

# Main

def main():
    meteomatics_user = "universityofstgallen_soerensen_johann"
    meteomatics_pass = "iDV83e4R6e"

    # Coordinates for St. Gallen, Switzerland
    location = (47.4245, 9.3767)

    service = google_calendar_service()

    weather_data = get_precipitation_data(meteomatics_user, meteomatics_pass, location)

    # Create calendar events
    if weather_data:
        create_weather_events(service, weather_data)
    else:
        print("No weather data available.")

# Run the script
if __name__ == "__main__":
    main()

   
