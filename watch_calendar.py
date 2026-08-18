import json
import os
import requests
from icalendar import Calendar

URL = "https://calendar.google.com/calendar/ical/6d8046cd0c770e72aa60ffb4ce82a2b68ac63ff7c9c015d1cab53a0661b7ced4@group.calendar.google.com/public/basic.ics"

STATE_FILE = "events.json"


PUSHOVER_USER = os.environ["PUSHOVER_USER"]
PUSHOVER_TOKEN = os.environ["PUSHOVER_TOKEN"]


def send_push(message):

    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER,
            "title": "XPS Watcher",
            "message": message,
        },
        timeout=30,
    )

    print(response.status_code)


def load_calendar():
    response = requests.get(URL)
    response.raise_for_status()

    calendar = Calendar.from_ical(response.text)

    events = {}

    for component in calendar.walk():

        if component.name != "VEVENT":
            continue

        uid = str(component.get("uid"))
        summary = str(component.get("summary"))
        start = str(component.get("dtstart").dt)

        end = ""

        if component.get("dtend"):
            end = str(component.get("dtend").dt)

        events[uid] = {
            "summary": summary,
            "start": start,
            "end": end
        }

    return events


def load_previous_state():

    if not os.path.exists(STATE_FILE):
        return None

    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(events):

    with open(STATE_FILE, "w") as f:
        json.dump(events, f, indent=2)


def compare_events(old_events, new_events):

    changes = []

    # Nye arrangementer
    for uid, event in new_events.items():

        if uid not in old_events:

            changes.append(
                f"NYTT ARRANGEMENT\n"
                f"{event['summary']}\n"
                f"Start: {event['start']}"
            )

    # Endrede arrangementer
    for uid, event in new_events.items():

        if uid not in old_events:
            continue

        old = old_events[uid]

        if (
            old["start"] != event["start"]
            or old["end"] != event["end"]
        ):

            changes.append(
                f"ENDRET ARRANGEMENT\n"
                f"{event['summary']}\n\n"
                f"Gammel start: {old['start']}\n"
                f"Ny start:    ['start' {event['start']}\n\n"
        f"Gammel slutt: {old['end']}\n"
                f"Ny slutt:     {event['end']}"
            )

    # Slettede arrangementer
    for uid, event in old_events.items():

        if uid not in new_events:

            changes.append(
                f"SLETTET ARRANGEMENT\n"
                f"{event['summary']}\n"
                f"Start: {event['start']}"
            )

    return changes


def main():

    current_events = load_calendar()

    previous_events = load_previous_state()

    if previous_events is None:

        save_state(current_events)

        print(
            "Første kjøring. "
            "Kalenderstatus lagret i events.json"
        )

        return

    changes = compare_events(
        previous_events,
        current_events
    )

    if changes:

        print("\n========== ENDRINGER ==========\n")

        for change in changes:
            print(change)
            print("\n---------------------------\n")

    else:

        print("Ingen endringer funnet.")

  send_push("🚀 Test fra GitHub XPS Watcher")

    save_state(current_events)


if __name__ == "__main__":
    main()
