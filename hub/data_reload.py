import csv
import json
import os
import re

SENSOR_RE = re.compile(r"sensor:\s*(?P<sensor>[^,]+),\s*characteristic:\s*(?P<characteristic>[^,]+),\s*value:\s*(?P<value>.+)$", re.IGNORECASE)
TRIGGER_RE = re.compile(r"trigger:\s*(?P<trigger>[^,]+),\s*activated:\s*(?P<activated>True|False)", re.IGNORECASE)
IMAGE_RE = re.compile(r"Image\s+(?P<path>.+?)\s+saved", re.IGNORECASE)

def data_reload(data_json_path, events_table_csv_path):
    """Update dashboard state from event-log rows not processed previously."""
    with open(data_json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    if not os.path.exists(events_table_csv_path):
        return
    with open(events_table_csv_path, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    last_event_line = int(data.get("last_event_line", 0) or 0)
    if last_event_line > len(rows):
        last_event_line = 0
    data["last_event_line"] = len(rows)

    for row in rows[last_event_line:]:
        location = (row.get("location") or "").strip()
        room_id = location.split("|", 1)[0]
        room = data.get("rooms", {}).get(room_id)
        if room is None:
            continue
        event = (row.get("event") or "").strip().lower()
        details = row.get("details") or ""
        if event == "sensor read":
            match = SENSOR_RE.search(details)
            if match:
                characteristic = match.group("characteristic").lower()
                value = match.group("value").strip()
                if "temp" in characteristic:
                    room["temperature"] = value
                elif "humid" in characteristic:
                    room["humidity"] = value
        elif event == "trigger":
            match = TRIGGER_RE.search(details)
            if match and "pir" in match.group("trigger").lower():
                room["movement"] = "Detected" if match.group("activated").lower() == "true" else "Not detected"
        elif event == "image saved":
            match = IMAGE_RE.search(details)
            if match:
                room["image_url"] = os.path.basename(match.group("path"))
    with open(data_json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
        file.write("\n")
