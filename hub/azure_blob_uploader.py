import csv
import datetime
import glob
import json
import os
from pathlib import Path
from azure.storage.blob import BlobServiceClient

def _current_dashboard_images(data_file_path):
    if not os.path.exists(data_file_path):
        return set()
    with open(data_file_path, encoding="utf-8") as file:
        data = json.load(file)
    current = set()
    for room in data.get("rooms", {}).values():
        image_url = room.get("image_url")
        if image_url:
            current.add(os.path.basename(str(image_url)))
    return current

def upload_to_azure(csv_file_path="events_table.csv", data_file_path="data.json"):
    """Archive local logs and images using credentials supplied at runtime."""
    timestamp = datetime.datetime.now().isoformat(timespec="seconds").replace(":", "-")
    connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING is not configured")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    csv_container_name = os.environ.get("AZURE_CSV_CONTAINER", "csv-logs")
    images_container_name = os.environ.get("AZURE_IMAGES_CONTAINER", "images")
    current_images = _current_dashboard_images(data_file_path)
    runtime_dir = Path(os.environ.get("WSN_RUNTIME_DIR", ".")).resolve()

    if os.path.exists(csv_file_path):
        blob_name = f"{timestamp}_{os.path.basename(csv_file_path)}"
        client = blob_service_client.get_blob_client(container=csv_container_name, blob=blob_name)
        with open(csv_file_path, "rb") as data:
            client.upload_blob(data, overwrite=True)
        os.remove(csv_file_path)
        with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
            csv.DictWriter(csvfile, fieldnames=["timestamp", "location", "event", "details"]).writeheader()
        print(f"Archived {blob_name} and reset {csv_file_path}")

    for jpg_file in glob.glob(str(runtime_dir / "*.jpg")):
        if os.path.basename(jpg_file) in current_images:
            continue
        client = blob_service_client.get_blob_client(container=images_container_name, blob=os.path.basename(jpg_file))
        with open(jpg_file, "rb") as data:
            client.upload_blob(data, overwrite=True)
        os.remove(jpg_file)
        print(f"Archived and deleted local image {jpg_file}")
