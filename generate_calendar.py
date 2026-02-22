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
    with open("cdl.ics", "w") as f:
        f.writelines(calendar)
    exit(0)

matches = soup.find_all("div", class_="match-card")

for match in matches:
    try:
        teams_tag = match.find("div", class_="teams")
        date_tag = match.find("div", class_="date")

        teams = teams_tag.text.strip() if teams_tag else "TBD vs TBD"
        if not date_tag:
            continue  # skip if no date

        date_str = date_tag.text.strip()

        # Try multiple date formats
        parsed = False
        for fmt in ("%B %d, %Y %I:%M %p", "%b %d, %Y %I:%M %p"):
            try:
                event_time = datetime.strptime(date_str, fmt)
                parsed = True
                break
            except ValueError:
                continue
        if not parsed:
            continue

        event = Event()
        event.name = f"CDL Match: {teams}"
        event.begin = event_time
        calendar.events.add(event)

    except Exception as e:
        print(f"Skipping match due to error: {e}")
        continue

with open("cdl.ics", "w") as f:
    f.writelines(calendar)

print("cdl.ics generated successfully with", len(calendar.events), "events.")
