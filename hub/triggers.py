import asyncio
from bleak import BleakClient, BleakScanner
import datetime
import csv


def trigger_ble(nodes, node_name, csv_file_name):
    node_details = nodes['triggers'][node_name]

    async def run():
        node_name = node_details["ble_name"]

        scanner = BleakScanner()

        device = await scanner.find_device_by_name(node_name)
        print(device)

        if device:
            return True

        return False

    loop = asyncio.get_event_loop()
    trigger_value = loop.run_until_complete(run())
    with open(csv_file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        row = [str(datetime.datetime.now()),
                            node_details['location'],
                            "trigger",
                            f"trigger: {node_name}, activated: {trigger_value}"]
        writer.writerow(row)
        print(row)
    return trigger_value

def distance_sensor_trigger(nodes, node_name, min_distance):
    node_details = nodes['distance_senors'][node_name]

    async def run():
        node_name = node_details["ble_name"]
        scanner = BleakScanner()

        device = None
        devices = await scanner.discover()
        for d in devices:
            if d.name.startswith(node_name):
                device = d
                name_and_dist = str(device).split(" ")[1]
                distance = name_and_dist.split("_")[1]
                return distance
                break

        if not device:
            print(f"No device found with name starting with {node_name}")
            return None

    trig_value = False
    loop = asyncio.get_event_loop()
    distance = loop.run_until_complete(run())
    if float(distance) <= int(min_distance):
        trig_value = True
        print(f"Distance sensor {node_name} triggered")

    return trig_value