import json
import csv

def data_reload(data_json_path, events_table_csv_path):
    # Load the JSON data from the file
    with open(data_json_path, 'r') as file:
        data = json.load(file)

    # Load the events table from the CSV file
    with open(events_table_csv_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        events_table_list = [line for line in reader]

    len_table = len(events_table_list)
    last_event_line = data['last_event_line']
    data['last_event_line'] = len_table
    events_table_list = events_table_list[(last_event_line+1):]

    for line in events_table_list:
        room = line[1]
        if "sensor: temp_humidA, characteristic: Temperature_sensor" in line[3]:
            temperature = line[3].split(" ")[-1]
            data['rooms'][room]["temperature"] = temperature

        if "sensor: temp_humidA, characteristic: Humidity_sensor" in line[3]:
            humidity = line[3].split(" ")[-1]
            data['rooms'][room]["humidity"] = humidity

        if "trigger: PIR_nodeA, activated: False" in line[3]:
            data['rooms'][room]["movement"] = "No detected"

        if "trigger: pirNoderoom1, activated: True" in line[3]:
            data['rooms'][room]["movement"] = "Detected"

        if "Image saved" in line[2]:
            image_path = line[3].split(" ")[-2]
            data['rooms'][room]["image_url"] = image_path
            #TODO: Add more events to the loop


    with open(data_json_path, 'w') as file:
        json.dump(data, file, indent=4)
