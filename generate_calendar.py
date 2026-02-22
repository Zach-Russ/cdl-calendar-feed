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
    print(f"Processing match #{i}: {match.get('team1', {}).get('name', 'TBD')} vs {match.get('team2', {}).get('name', 'TBD')}")
    try:
        # Sometimes the API uses 'date' or 'datetime' or 'start_time'
        date_str = match.get("date") or match.get("datetime") or match.get("start_time")
        if not date_str:
            print("  Skipping: no date field found")
            continue

        # Try parsing ISO format first
        try:
            event_time = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except Exception:
            # Fallback: just skip if not parseable
            print(f"  Skipping: could not parse date '{date_str}'")
            continue

        event = Event()
        team1 = match.get("team1", {}).get("name", "TBD")
        team2 = match.get("team2", {}).get("name", "TBD")
        event.name = f"CDL Match: {team1} vs {team2}"
        event.begin = event_time

        calendar.events.add(event)
        events_added += 1
        print(f"  Added event at {event_time}")

    except Exception as e:
        print(f"  Skipping match due to error: {e}")

with open("cdl.ics", "w") as f:
    f.writelines(calendar)

print(f"ICS generated with {events_added} events.")
