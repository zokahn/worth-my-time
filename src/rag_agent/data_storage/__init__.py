import json
import os
from datetime import datetime

def store_activity(activity):
    "Store the activity data in a JSON file"

    # Get the current date
    date = datetime.now().strftime('%Y-%m-%d')

    # Create the directory for storing the data if it doesn't exist
    os.makedirs('data', exist_ok=True)

    # Define the path to the JSON file
    file_path = os.path.join('data', f'{date}.json')

    # Load the existing data
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    # Add the new activity to the data
    data.append(activity)

    # Save the data
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def store_status_file(filename, content):
    "Store the status file content"
    
    # Create the directory for storing the status files if it doesn't exist
    os.makedirs('data/status', exist_ok=True)

    # Define the path to the JSON file
    file_path = os.path.join('data/status', f'{filename}.json')

    # Create a dictionary with the file content and timestamp
    status_data = {
        'filename': filename,
        'content': content,
        'timestamp': datetime.now().isoformat()
    }

    # Save the data
    with open(file_path, 'w') as file:
        json.dump(status_data, file, indent=4)
