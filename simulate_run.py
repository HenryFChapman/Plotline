import os
import time
import secrets
import string
import shutil

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

def move_file(name):
	# Define paths
	source_file = 'Sample Dataset.json'
	new_filename = f'{name}.json'
	target_folder = 'plotline_data'

	# Ensure target folder exists
	os.makedirs(target_folder, exist_ok=True)

	# Construct full destination path
	destination_path = os.path.join(target_folder, new_filename)

	# Copy and rename the file
	shutil.copyfile(source_file, destination_path)

def clean_folder():
	# Folder to clean
	folder = 'plotline_data'

	# List of allowed filenames
	allowed_files = {
	    'Goodreads Data.json',
	    'News Summary.json',
	    'The Lord of the Rings.json',
	    'Datadog.json'
	}

	# Delete files not in the allowed list
	for filename in os.listdir(folder):
	    file_path = os.path.join(folder, filename)
	    if os.path.isfile(file_path) and filename not in allowed_files:
	        os.remove(file_path)

def simulate(dataset_id, name, upload):
	clean_folder()

	if upload.lower() == 'yes':
		upload_data()

	get_dataset_id()
	get_nested_narratives()
	move_file(name)
	print(f"Saved: plotline_data/{name}.json")
	return

