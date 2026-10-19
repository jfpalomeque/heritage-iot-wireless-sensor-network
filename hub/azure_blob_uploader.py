import csv
import datetime
import glob
import json
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def upload_to_azure(csv_file_path="events_table.csv", data_file_path="data.json"):
    """Archive local logs and images using credentials supplied at runtime.

    Required environment variable: ``AZURE_STORAGE_CONNECTION_STRING``.
    Optional container variables: ``AZURE_CSV_CONTAINER`` and
    ``AZURE_IMAGES_CONTAINER``.
    """
    timestamp = str(datetime.datetime.now())
    connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING is not configured")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    csv_container_name = os.environ.get("AZURE_CSV_CONTAINER", "csv-logs")
    images_container_name = os.environ.get("AZURE_IMAGES_CONTAINER", "images")

    # Get the list of image URLs from data.json
    with open(data_file_path) as f:
        data = json.load(f)
        image_urls = [data["rooms"]["room1"]["image_url"]]

    # Upload the events_table.csv file to the csv-logs container
    if os.path.exists(csv_file_path):
        csv_blob_client = blob_service_client.get_blob_client(container=csv_container_name, blob=f'{timestamp}_{csv_file_path}')
        with open(csv_file_path, "rb") as data:
            csv_blob_client.upload_blob(data, overwrite=True)
        print(f"Uploaded {timestamp}_{csv_file_path} to {csv_container_name}")

    # Delete the events_table.csv file
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
        print(f"Deleted {csv_file_path}")

        # Create a new events_table.csv file with specified columns
        new_columns = ['timestamp', 'location', 'event', 'details']
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=new_columns)
            writer.writeheader()
        print(f"Created new {new_csv_file_path} with columns {new_columns}")

    # Upload all .jpg files to the images container except those in image_urls
    jpg_files = glob.glob("*.jpg")
    for jpg_file in jpg_files:
        if os.path.basename(jpg_file) not in image_urls:
            jpg_blob_client = blob_service_client.get_blob_client(container=images_container_name, blob=os.path.basename(jpg_file))
            with open(jpg_file, "rb") as data:
                jpg_blob_client.upload_blob(data, overwrite=True)
            print(f"Uploaded {jpg_file} to {images_container_name}")

    # Delete .jpg files except those in image_urls
    for jpg_file in jpg_files:
        if os.path.basename(jpg_file) not in image_urls:
            os.remove(jpg_file)
            print(f"Deleted {jpg_file}")
