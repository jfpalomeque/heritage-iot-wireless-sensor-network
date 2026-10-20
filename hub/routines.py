import asyncio
import csv
import datetime

import requests
from bleak import BleakClient, BleakScanner

def read_sensor(nodes, node_name, characteristic_name, csv_file_name):
    node_details = nodes["continuous_sensing_devices"][node_name]
    characteristic_details = node_details["characteristics"][characteristic_name]

    async def run():
        ble_name = node_details["ble_name"]
        characteristic_uuid = characteristic_details["characteristic_UUID"]
        device = await BleakScanner().find_device_by_name(ble_name)

        if not device:
            print(f"No device found with name {ble_name}")
            return None, None

        client = BleakClient(device, timeout=50.0)
        try:
            await client.connect()
            value = await client.read_gatt_char(characteristic_uuid)
            try:
                decoded_value = value.decode("utf-8")
            except UnicodeDecodeError:
                decoded_value = None
            return value, decoded_value
        except Exception as error:
            print(f"Failed to connect or read characteristic: {error}")
            return None, None
        finally:
            if client.is_connected:
                await client.disconnect()

    raw_value, decoded_value = asyncio.get_event_loop().run_until_complete(run())
    value_for_log = decoded_value if decoded_value is not None else raw_value

    with open(csv_file_name, "a", newline="") as csvfile:
        row = [
            str(datetime.datetime.now()),
            node_details["location"],
            "sensor read",
            f"sensor: {node_name}, characteristic: {characteristic_name}, value: {value_for_log}",
        ]
        csv.writer(csvfile).writerow(row)
        print(row)

def net_request(address, csv_file_name):
    response = requests.get(address, timeout=25)
    with open(csv_file_name, "a", newline="") as csvfile:
        row = [
            str(datetime.datetime.now()),
            "NA",
            "net request",
            f"request to address: {address}, status code: {response.status_code}",
        ]
        csv.writer(csvfile).writerow(row)
        print(row)
