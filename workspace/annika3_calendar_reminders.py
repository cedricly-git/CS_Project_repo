import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scope required
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_watering_event(service, plant_name, start_date, interval_days):
    """
    Create a recurring Google Calendar event to water a plant.
    """
    # Define the event start and end times (1-hour duration)
    start = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
    end = start + datetime.timedelta(hours=1)

    event = {
        'summary': f'Water {plant_name}',
        'description': f'Reminder to water your {plant_name}.',
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': 'Europe/Berlin',
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': 'Europe/Berlin',
        },
        'recurrence': [
            f'RRULE:FREQ=DAILY;INTERVAL={interval_days};COUNT=10'
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    # Insert the event into the user's primary calendar
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Created event for {plant_name}: {created_event.get('htmlLink')}")

def main():
    """Authenticate and add watering events based on plant data."""

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Calendar API service
    service = build('calendar', 'v3', credentials=creds)

