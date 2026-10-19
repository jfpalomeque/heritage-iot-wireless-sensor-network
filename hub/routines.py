import asyncio
from bleak import BleakClient, BleakScanner
import datetime
import csv
import requests


def read_sensor(nodes, node_name, characteristic_name, csv_file_name):
    node_details = nodes['continuous_sensing_devices'][node_name]
    characteristic_details = node_details['characteristics'][characteristic_name]

    async def run():
        node_name = node_details["ble_name"]
        characteristic_uuid = characteristic_details["characteristic_UUID"]

        scanner = BleakScanner()

        device = await scanner.find_device_by_name(node_name)

        if not device:
            print(f"No device found with name {node_name}")
            return None

        client = BleakClient(device, timeout=50.0)
        try:
            await client.connect()
            print(f"Connected: {client.is_connected}")

            # Read the specific characteristic
            value = await client.read_gatt_char(characteristic_uuid)
            raw_value = value  # Save the raw value
            decoded_value = None

            try:
                decoded_value = value.decode('utf-8')
            except UnicodeDecodeError:
                print(f"Value could not be decoded as UTF-8")

            return raw_value, decoded_value

        except Exception as e:
            print(f"Failed to connect or read characteristic: {e}")
            return None, None
        finally:
            await client.disconnect()
            print("Disconnected")

    loop = asyncio.get_event_loop()
    raw_value, decoded_value = loop.run_until_complete(run())

    with open(csv_file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if decoded_value != None:
            row = [str(datetime.datetime.now()),
                              node_details['location'],
                              "sensor read",
                              f"sensor: {node_name}, characteristic: {characteristic_name}, value: {decoded_value}"]
            writer.writerow(row)
            print(row)
        else:
            row = [str(datetime.datetime.now()),
                              node_details['location'],
                              "sensor read",
                              f"sensor: {node_name}, characteristic: {characteristic_name}, value: {raw_value}"]
            writer.writerow(row)
            print(row)

def net_request(address, csv_file_name):
    r = requests.get(address)
    with open(csv_file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        row = [str(datetime.datetime.now()),
                            'NA',
                            "net request",
                            f"request to address: {address}, status code: {r.status_code}"]
        writer.writerow(row)
        print(row)
