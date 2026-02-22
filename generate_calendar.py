import requests
import os
from ics import Calendar, Event
from datetime import datetime

API_KEY = os.environ.get("CITO_API_KEY")

if not API_KEY:
    print("ERROR: CITO_API_KEY not set")
    exit(1)

URL = "https://api.citoapi.com/v1/cod/cdl/schedule"
headers = {"x-api-key": API_KEY}

print("Fetching CDL schedule...")
response = requests.get(URL, headers=headers, timeout=15)
print("Status Code:", response.status_code)
response.raise_for_status()

data = response.json()
matches = data.get("data", [])
print(f"Matches returned by API: {len(matches)}")

calendar = Calendar()
events_added = 0

for i, match in enumerate(matches, start=1):
    try:
        team1 = match.get("homeTeamName", "TBD")
        team2 = match.get("awayTeamName", "TBD")
        date_str = match.get("matchDate")  # use the correct field

        if not date_str:
            print(f"Match #{i} skipped: no matchDate field")
            continue

        # Convert ISO format to datetime
        event_time = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

        event = Event()
        event.name = f"CDL Match: {team1} vs {team2}"
        event.begin = event_time

        calendar.events.add(event)
        events_added += 1
        print(f"Added Match #{i}: {team1} vs {team2} at {event_time}")

    except Exception as e:
        print(f"Skipping Match #{i} due to error: {e}")

with open("cdl.ics", "w") as f:
    f.writelines(calendar)

print(f"ICS generated with {events_added} events.")
