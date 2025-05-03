# Required for compatibility with Python
from __future__ import print_function

# Standard Python modules for date/time and file handling
import datetime
import os.path

# Google libraries for API authentication and communication
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scope of application
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """
    Connects to the Google Calendar API and prints the next 10 events
    from the user's primary calendar.
    """
# storing of user credentials
    creds = None  

    # Check if token.json file exists
    if os.path.exists('token.json'):
        # Loading of saved credentials
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials, start a new login flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh the expired token automatically
            creds.refresh(Request())
        else:
            # Start a new OAuth login session using credentials.json
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the new token for next time to avoid logging in again
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the connection to the Google Calendar API service
    service = build('calendar', 'v3', credentials=creds)

    # Get the current time in UTC
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    print('Getting the upcoming 10 events')

    # Make an API call to fetch the next 10 events from the user's primary calendar
    events_result = service.events().list(
        calendarId='primary',       # 'primary' = default calendar
        timeMin=now,                # Only events after this moment
        maxResults=10,              # Limit to 10 events
        singleEvents=True,          # Only return single instances of repeating events
        orderBy='startTime'         # Sort results by start time
    ).execute()

    # Get the 'items' list from the response (each item = an event)
    events = events_result.get('items', [])

    # If no events were found, print a message
    if not events:
        print('No upcoming events found.')
    # Otherwise, loop through events and print details
    for event in events:
        # Get the event start time; could be 'dateTime' or 'date' (for all-day events)
        start = event['start'].get('dateTime', event['start'].get('date'))
        # Print the event start time and summary (title)
        print(start, event['summary'])

# This makes sure the script runs only when executed directly, not when imported
if __name__ == '__main__':
    main()
