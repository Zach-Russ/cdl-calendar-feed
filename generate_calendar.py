import requests
import os
from ics import Calendar, Event
from datetime import datetime, timedelta

# Get API key from environment
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
        # Correct team names from API
        team1 = match.get("homeTeamName", "TBD")
        team2 = match.get("awayTeamName", "TBD")
        date_str = match.get("matchDate")

        if not date_str:
            print(f"Match #{i} skipped: no matchDate field")
            continue

        # Convert ISO string to datetime
        event_time = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

        event = Event()
        event.name = f"CDL Match: {team1} vs {team2}"
        event.begin = event_time
        event.end = event_time + timedelta(hours=1)  # Explicit end time for 1 hour

        # Optional: add stage, round, stream URL to description
        stage = match.get("stage") or "TBD"
        round_info = match.get("round") or "TBD"
        stream = match.get("streamUrl") or "N/A"
        event.description = f"Stage: {stage}\nRound: {round_info}\nStream: {stream}"

        calendar.events.add(event)
        events_added += 1
        print(f"Added Match #{i}: {team1} vs {team2} at {event_time}")

    except Exception as e:
        print(f"Skipping Match #{i} due to error: {e}")

# Write ICS file
with open("cdl.ics", "w") as f:
    f.writelines(calendar)

print(f"ICS generated with {events_added} events.")
