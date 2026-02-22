import requests
from ics import Calendar, Event
from datetime import datetime
import pytz
import os

# Get API key from environment variable
API_KEY = os.environ.get("CITO_API_KEY")
if not API_KEY:
    raise ValueError("CITO_API_KEY is not set in environment variables!")

# URL for the CDL schedule
URL = "https://api.citoapi.com/v1/cod/cdl/schedule"

headers = {"x-api-key": API_KEY}

calendar = Calendar()

try:
    response = requests.get(URL, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print(f"Error fetching CDL schedule: {e}")
    with open("cdl.ics", "w") as f:
        f.writelines(calendar)
    exit(0)

events_added = 0
for match in data.get("data", []):
    try:
        team1 = match.get("team1", {}).get("name", "TBD")
        team2 = match.get("team2", {}).get("name", "TBD")
        date_iso = match.get("date")
        if not date_iso:
            continue

        # Parse ISO date
        dt = datetime.fromisoformat(date_iso.replace("Z", "+00:00"))

        event = Event()
        event.name = f"CDL Match: {team1} vs {team2}"
        event.begin = dt
        calendar.events.add(event)
        events_added += 1
    except Exception as e:
        print(f"Skipping match due to error: {e}")
        continue

with open("cdl.ics", "w") as f:
    f.writelines(calendar)

print(f"cdl.ics generated successfully with {events_added} events.")