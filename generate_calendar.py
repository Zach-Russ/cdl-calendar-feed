import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime
import pytz

URL = "https://callofdutyleague.com/en-us/schedule"
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

calendar = Calendar()

matches = soup.find_all("div", class_="match-card")

for match in matches:
    teams = match.find("div", class_="teams").text.strip()
    date_str = match.find("div", class_="date").text.strip()

    event = Event()
    event.name = f"CDL Match: {teams}"
    event.begin = datetime.strptime(date_str, "%B %d, %Y %I:%M %p")
    event.make_all_day()

    calendar.events.add(event)

with open("cdl.ics", "w") as f:
    f.writelines(calendar)
