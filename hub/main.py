from cron_converter import Cron
import csv
import datetime
import json
import os
import time

from routines import *
from triggers import *
from actions import *
from azure_blob_uploader import *

csv_file_name = os.environ.get("WSN_EVENTS", "events_table.csv")
columns = ["timestamp", "location", "event", "details"]

if not os.path.exists(csv_file_name):
    with open(csv_file_name, "w", newline="") as csvfile:
        csv.DictWriter(csvfile, fieldnames=columns).writeheader()

wsn_conf_file = os.environ.get("WSN_CONFIG", "wsn_config.json")
nodes = None
routines = None
actions = None
last_file_modification = None
last_cron_reference = datetime.datetime(1970, 1, 1)

while True:
    try:
        tmtime = os.path.getmtime(wsn_conf_file)
    except FileNotFoundError:
        print("Configuration file not found. Check WSN_CONFIG and try again.")
        break

    if tmtime != last_file_modification:
        try:
            with open(wsn_conf_file, "r", encoding="utf-8") as file:
                config = json.load(file)
        except json.JSONDecodeError:
            print("JSON configuration is not formatted correctly.")
            break

        last_file_modification = tmtime
        nodes = config["nodes"]
        routines = config["routines"]
        actions = config["actions"]

    cron_instance = Cron()
    cron_reference = datetime.datetime.now()

    for routine in routines:
        cron_instance.from_string(routine["schedule"])
        schedule = cron_instance.schedule(cron_reference)
        previous_run = schedule.prev()
        if last_cron_reference < previous_run <= cron_reference:
            print(f"Executing routine {routine['name']}")
            try:
                exec(routine["script"])
            except Exception as error:
                with open(csv_file_name, "a", newline="") as csvfile:
                    row = [
                        str(datetime.datetime.now()),
                        routine["location"],
                        "routine error",
                        f"routine: {routine['name']} failed with error: {error}",
                    ]
                    csv.writer(csvfile).writerow(row)
                    print(row)

    for action in actions:
        print(f"Checking action {action['name']}")
        trigger_value = False
        try:
            exec(action["trigger"])
        except Exception as error:
            with open(csv_file_name, "a", newline="") as csvfile:
                row = [
                    str(datetime.datetime.now()),
                    action["location"],
                    "action error",
                    f"Trigger for action: {action['name']} failed with error: {error}",
                ]
                csv.writer(csvfile).writerow(row)
                print(row)
            continue

        if trigger_value is True:
            try:
                exec(action["script"])
            except Exception as error:
                with open(csv_file_name, "a", newline="") as csvfile:
                    row = [
                        str(datetime.datetime.now()),
                        action["location"],
                        "action error",
                        f"action: {action['name']} failed with error: {error}",
                    ]
                    csv.writer(csvfile).writerow(row)
                    print(row)
        else:
            print(f"Action {action['name']} not triggered")

    last_cron_reference = cron_reference
    time.sleep(1)
