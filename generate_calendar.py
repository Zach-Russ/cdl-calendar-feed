import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime
import pytz
import os

URL = "https://callofdutyleague.com/en-us/schedule"
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

calendar = Calendar()

matches = soup.find_all("div", class_="match-card")

for match in matches:
    teams_tag = match.find("div", class_="teams")
    date_tag = match.find("div", class_="date")
    if not teams_tag or not date_tag:
        continue  # Skip if info not available

    teams = teams_tag.text.strip()
    date_str = date_tag.text.strip()

    try:
        event = Event()
        event.name = f"CDL Match: {teams}"
        event.begin = datetime.strptime(date_str, "%B %d, %Y %I:%M %p")
        event.make_all_day()
        calendar.events.add(event)
    except Exception as e:
        print(f"Skipping event due to error: {e}")

# Save the file in the root so workflow can publish it
with open("cdl.ics", "w") as f:
    f.writelines(calendar)

print("cdl.ics generated successfully.")
