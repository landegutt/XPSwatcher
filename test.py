import requests
from icalendar import Calendar

url = "https://calendar.google.com/calendar/ical/6d8046cd0c770e72aa60ffb4ce82a2b68ac63ff7c9c015d1cab53a0661b7ced4@group.calendar.google.com/public/basic.ics"

response = requests.get(url)
response.raise_for_status()

calendar = Calendar.from_ical(response.text)

for component in calendar.walk():
    if component.name == "VEVENT":
        print("Aktivitet:", component.get("summary"))
        print("Start:", component.get("dtstart").dt)
        print("-" * 40)
