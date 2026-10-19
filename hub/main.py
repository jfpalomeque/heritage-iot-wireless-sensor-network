from cron_converter import Cron
import datetime
import os
import json
import time
import csv

from routines import *
from triggers import *
from actions import *
from azure_blob_uploader import *


csv_file_name = "events_table.csv"
columns = ['timestamp', 'location', 'event', 'details']

file_exists = os.path.exists(csv_file_name)

if not file_exists:
    with open(csv_file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()


wsn_conf_file = os.environ.get('WSN_CONFIG', 'wsn_config.json')

nodes = None
routines = None
actions = None
last_file_modification = None
last_cron_reference = datetime.datetime(1970, 1, 1)




while True:
    tmtime = os.path.getmtime(wsn_conf_file)
    if tmtime != last_file_modification:
        try:
            with open(wsn_conf_file, 'r') as file:
                config = json.load(file)
        except FileNotFoundError:
            print("File not found. Please check the file path and try again.")
            break
        except json.JSONDecodeError:
            print("JSON file is not formatted correctly. Please check the file and try again.")
            break
        last_file_modification = tmtime

        nodes = config["nodes"]
        routines = config["routines"]
        actions = config["actions"]


    cron_instance = Cron()
    cron_reference = datetime.datetime.now()

    for routine in routines:
        cron_instance.from_string(routine['schedule'])
        schedule = cron_instance.schedule(cron_reference)
        if schedule.prev() > last_cron_reference and schedule.prev() <= cron_reference:
            print(f"Executing routine {routine['name']}")
            try:
                exec(routine['script'])
            except Exception as e:
                with open(csv_file_name, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    row = [str(datetime.datetime.now()),
                                    routine['location'],
                                    "routine error",
                                    f"routine: {routine['name']} failed with error: {e}"]
                    writer.writerow(row)
                    print(row)

    trigger_value = None
    for action in actions:
        print(f"Checking action {action['name']}")
        try:
            exec(action['trigger'])
        except Exception as e:
            with open(csv_file_name, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                row = [str(datetime.datetime.now()),
                                action['location'],
                                "action error",
                                f"Trigger for action: {action['name']} failed with error: {e}"]
                writer.writerow(row)
                print(row)
        if trigger_value == True:
            try:
                exec(action['script'])
            except Exception as e:
                with open(csv_file_name, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    row = [str(datetime.datetime.now()),
                                    action['location'],
                                    "action error",
                                    f"action: {action['name']} failed with error: {e}"]
                    writer.writerow(row)
                    print(row)
        else:
            print(f"Action {action['name']} not triggered")

    last_cron_reference = cron_reference
    time.sleep(1)
