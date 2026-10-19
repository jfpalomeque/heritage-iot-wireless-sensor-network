import requests
import base64
from PIL import Image
from io import BytesIO
import datetime
import csv
import time
import asyncio
import os
from bleak import BleakScanner
from AI_image_analysers import *




def take_save_delete_image(nodes, cam_name, csv_file_name):
    cam_details = nodes['cam_nodes'][cam_name]
    cam_ip = cam_details["ip_address"]

    delete_url = cam_ip + "/delete"

# Capture image URL
    capture_url = cam_ip + "/capture"


    # Download image URL
    download_url = cam_ip + "/download"

    # Delete image URL
    delete_url = cam_ip + "/delete"
    capture_response = requests.get(capture_url, timeout=25)
    if capture_response.status_code == 200:
        time.sleep(2)
        download_response = requests.get(download_url, timeout=25)
        if download_response.status_code == 200:
            image_data = download_response.text.split(",")[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            image_file_name = f"image_{cam_name}_{str(datetime.datetime.now()).replace(' ','_')}.jpg"
            image.save(image_file_name)
            print("Image saved")
            time.sleep(2)
            delete_response = requests.get(delete_url, timeout=25)
            print(delete_response.status_code)

            row_data = [str(datetime.datetime.now()),
                                    cam_details['location'],
                                    "Image saved",
                                    f"Image {image_file_name} saved"]
            with open(csv_file_name, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row_data)
                print(row_data)

            #label, model = CLIP_analyze_image(image_file_name, "image_labels.json")
            labels_path = os.environ.get("IMAGE_LABELS_PATH", "image_labels.json")
            model_path = os.environ.get("VIT_MODEL_PATH", "ai_image_classifiers_models/vit_multiple")
            label, model = VIT_analyze_image_multilabel(image_file_name, labels_path, model_path)


            if label == "negative":
                print(f"Image {image_file_name} labeled as {label} by {model} | ALARM!")
                row_data = [str(datetime.datetime.now()),
                                    cam_details['location'],
                                    "Image analysed",
                                    f"Image {image_file_name} labeled as {label} by {model} | ALARM!"]

            if label == "positive":
                print(f"Image {image_file_name} labeled as {label} by {model} | OK")
                row_data = [str(datetime.datetime.now()),
                                        cam_details['location'],
                                        "Image analysed",
                                        f"Image {image_file_name} labeled as {label} by {model} | OK"]

            with open(csv_file_name, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row_data)
                print(row_data)





    else:
        row_data = [str(datetime.datetime.now()),
                                    cam_details['location'],
                                    "error camera",
                                    f"Failed to capture image from {cam_name}"]

        with open(csv_file_name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row_data)
            print(row_data)


def distance_sensor_reading(nodes, node_name, csv_file_name):
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

    loop = asyncio.get_event_loop()
    distance = loop.run_until_complete(run())

    with open(csv_file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if distance != None:
            row = [str(datetime.datetime.now()),
                              f"{node_details['location']}|{node_details['cabinet']}",
                              "distance_sensor_reading",
                              f"distance sensor: {node_name}, distance: {distance}cm"]
            writer.writerow(row)
            print(row)

def write_row(location, value, csv_file_name):

    with open(csv_file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        row = [str(datetime.datetime.now()),
                            location,
                            "writen",
                            value]
        writer.writerow(row)
        print(row)
