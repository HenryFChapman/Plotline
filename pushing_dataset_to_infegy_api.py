import requests
import json
import csv
from urllib.parse import urlencode
import os

# Base URL for Custom Datset API (Atlas)
INFEGY_ATLAS_API_BASE_URL = "https://atlas.infegy.com/api/v3"

# Infegy Atlas API Key
INFEGY_ATLAS_API_KEY = open("infegy_atlas_api_key.txt").read().strip()

# Set headers for requests
ATLAS_HEADERS = {
  "Content-Type": "application/json",
}

# Function to get the details of a dataset by a specific dataset ID
def get_dataset_by_id(dataset_id):
    base_url = f'{INFEGY_ATLAS_API_BASE_URL}/custom-dataset/list'

    params = {
        'api_key': INFEGY_ATLAS_API_KEY
    }

    url = f"{base_url}?{urlencode(params)}"

    response = requests.get(url)
    response.raise_for_status()

    response = response.json()

    # Find the dataset matching the specified ID
    for dataset in response['output']:
        if dataset["id"] == dataset_id:
            return dataset

    return None

# Function to read CSV and convert it to JSON in the correct format our API will understand.
def csv_to_json(csv_file_path):

    # Open the CSV file for reading
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csv_file)

        # Convert each row in the CSV file into a dictionary and add it to a list
        data = []
        for row in csv_reader:
            data.append(row)

    json_data = {"content":data}

    return json_data

# Function to generate the correct field mapping configuration configuration
def generate_mapping():
    mapping = {
        "columns": [
            {"name": "Video_Title", "type": "keyword"},
            {"name": "Video_Date", "type": "timestamp"},
            {"name": "Video_URL", "type": "text"},
            {"name": "Comment_Timestamp", "type":"timestamp"},
            {"name": "Comment_Author", "type": "keyword"},
            {"name": "Comment_Text", "type": "text", "traits":{"analyze": True}},
        ]
    }
    return mapping

def create_dataset(mapping, dataset_title):
  base_url = f'{INFEGY_ATLAS_API_BASE_URL}/custom-dataset?&api_key={INFEGY_ATLAS_API_KEY}&title={dataset_title}'

  params = {
      'api_key': INFEGY_ATLAS_API_KEY,
      'title': dataset_title
  }

  url = f"{base_url}?{urlencode(params)}"
  response = requests.post(url, data=json.dumps(mapping)).json()

  return response['output']['id']

# Function to upload content to the API
def upload_data(dataset_id, data):

    # API URL for uploading content
    base_url = f'{INFEGY_ATLAS_API_BASE_URL}/custom-dataset/content'

    params = {
        'api_key':INFEGY_ATLAS_API_KEY,
        'dry_run': 0,
        'id': dataset_id,
        'ignore_errors': 0
    }

    url = f"{base_url}?{urlencode(params)}"

    # Send the POST request to upload the content
    response = requests.post(url, headers=ATLAS_HEADERS, data=json.dumps(data)).json()

# If you have already initialized a dataset, fill in the dataset key here.
def push_data(dataset_name, dataset_id=""):

    #This function checks to see whether that dataset has already been initialized or not
    dataset = get_dataset_by_id(dataset_id)

    for temp_file in os.listdir("csvs"):
        if ".DS_Store" in temp_file:
            continue

        # Read the CSV file and convert it to Python dictionary.
        print("\t" + temp_file)

        try:
            data = csv_to_json("csvs/" + temp_file)
        except Exception:
            continue

        #This function checks to see whether that dataset has already been initialized or not
        dataset = get_dataset_by_id(dataset_id)

        # If dataset doesn't exists, initialize it with mapping.
        if not dataset:
            # Generate mapping to initialize dataset.
            mapping = generate_mapping()

            # Create a new dataset based on those mapping parameters
            dataset_id = create_dataset(mapping, dataset_name)

            # Upload new data to that dataset.
            upload_data(dataset_id, data)

        # Otherwise, upload data to that dataset.
        else:
            upload_data(dataset['id'], data)
