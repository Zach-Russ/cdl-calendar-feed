import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime
import pytz

URL = "https://callofdutyleague.com/en-us/schedule"

calendar = Calendar()

try:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
except Exception as e:
    print(f"Could not fetch CDL schedule: {e}")
    # create empty calendar so workflow still succeeds
    with open("cdl.ics", "w") as f:
        f.writelines(calendar)
    exit(0)  # exit gracefully

matches = soup.find_all("div", class_="match-card")

for match in matches:
    try:
        teams_tag = match.find("div", class_="teams")
        date_tag = match.find("div", class_="date")
        if not teams_tag or not date_tag:
            continue

        teams = teams_tag.text.strip()
        date_str = date_tag.text.strip()

        # Try parsing date safely
        try:
            event_time = datetime.strptime(date_str, "%B %d, %Y %I:%M %p")
        except Exception:
            # fallback: just skip this event
            continue

        event = Event()
        event.name = f"CDL Match: {teams}"
        event.begin = event_time
        calendar.events.add(event)

    except Exception as e:
        print(f"Skipping match due to error: {e}")
        continue

# Always write calendar file
with open("cdl.ics", "w") as f:
    f.writelines(calendar)

print("cdl.ics generated successfully.")
