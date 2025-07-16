import os
import time
import secrets
import string
from get_data import generate_manifest

def generate_token(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def upload_data():
	print("Uploading Data...")
	for filename in os.listdir("csvs"):

		if ".DS_Store" in filename:
			continue

		print("\t" + filename)
		time.sleep(.5)
	print("Finished Uploading Data...")

def get_dataset_id():
	print("Dataset ID: ds_5y1JwG9zkX6")
	return

def get_nested_narratives():
	for narrative in range(0, 5):
		token = generate_token()
		print(f"Token retrieved:	 {token}")
		time.sleep(.5)

def simulate_run(dataset_id, name):
	upload_data()
	get_dataset_id()
	get_nested_narratives()
	print(f"Saved: plotline_data/{name}.json")
	generate_manifest()
	return