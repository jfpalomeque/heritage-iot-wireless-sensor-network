import asyncio
import base64
import csv
import datetime
import os
import time
from io import BytesIO

import requests
from bleak import BleakScanner
from PIL import Image

from AI_image_analysers import VIT_analyze_image_multilabel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUNTIME_DIR = os.path.abspath(os.environ.get("WSN_RUNTIME_DIR", BASE_DIR))
DEFAULT_LABELS_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "configs", "image_labels.json"))
os.makedirs(RUNTIME_DIR, exist_ok=True)

def take_save_delete_image(nodes, cam_name, csv_file_name):
    cam_details = nodes["cam_nodes"][cam_name]
    cam_ip = cam_details["ip_address"]

    capture_response = requests.get(cam_ip + "/capture", timeout=25)
    if capture_response.status_code != 200:
        row_data = [str(datetime.datetime.now()), cam_details["location"], "error camera", f"Failed to capture image from {cam_name}"]
        with open(csv_file_name, "a", newline="") as csvfile:
            csv.writer(csvfile).writerow(row_data)
        return

    time.sleep(2)
    download_response = requests.get(cam_ip + "/download", timeout=25)
    if download_response.status_code != 200:
        row_data = [str(datetime.datetime.now()), cam_details["location"], "error camera", f"Failed to download image from {cam_name}"]
        with open(csv_file_name, "a", newline="") as csvfile:
            csv.writer(csvfile).writerow(row_data)
        return

    image_data = download_response.text.split(",", 1)[1]
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image_basename = f"image_{cam_name}_{str(datetime.datetime.now()).replace(' ', '_')}.jpg"
    image_file_name = os.path.join(RUNTIME_DIR, image_basename)
    image.save(image_file_name)

    time.sleep(2)
    requests.get(cam_ip + "/delete", timeout=25)

    row_data = [str(datetime.datetime.now()), cam_details["location"], "Image saved", f"Image {image_basename} saved"]
    with open(csv_file_name, "a", newline="") as csvfile:
        csv.writer(csvfile).writerow(row_data)

    labels_path = os.environ.get("IMAGE_LABELS_PATH", DEFAULT_LABELS_PATH)
    model_path = os.environ.get("VIT_MODEL_PATH")
    if not model_path:
        raise RuntimeError("VIT_MODEL_PATH must point to a local fine-tuned model directory before image classification is enabled")

    label, model = VIT_analyze_image_multilabel(image_file_name, labels_path, model_path)
    if label == "negative":
        message = f"Image {image_basename} labeled as {label} by {model} | ALARM!"
    elif label == "positive":
        message = f"Image {image_basename} labeled as {label} by {model} | OK"
    else:
        message = f"Image {image_basename} could not be classified by {model}"

    row_data = [str(datetime.datetime.now()), cam_details["location"], "Image analysed", message]
    with open(csv_file_name, "a", newline="") as csvfile:
        csv.writer(csvfile).writerow(row_data)

def distance_sensor_reading(nodes, node_name, csv_file_name):
    node_details = nodes["distance_senors"][node_name]
    async def run():
        ble_name = node_details["ble_name"]
        devices = await BleakScanner.discover()
        for device in devices:
            if device.name and device.name.startswith(ble_name):
                return str(device).split(" ")[1].split("_")[1]
        return None
    distance = asyncio.get_event_loop().run_until_complete(run())
    if distance is not None:
        row = [str(datetime.datetime.now()), f"{node_details['location']}|{node_details['cabinet']}", "distance_sensor_reading", f"distance sensor: {node_name}, distance: {distance}cm"]
        with open(csv_file_name, "a", newline="") as csvfile:
            csv.writer(csvfile).writerow(row)

def write_row(location, value, csv_file_name):
    row = [str(datetime.datetime.now()), location, "writen", value]
    with open(csv_file_name, "a", newline="") as csvfile:
        csv.writer(csvfile).writerow(row)
