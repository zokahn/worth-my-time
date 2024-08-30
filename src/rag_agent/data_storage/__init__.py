import json
import os
from datetime import datetime
from src.rag_agent.utils.logging_config import logger
from src.rag_agent.config import DATA_DIR, STATUS_DIR, SUMMARIES_DIR

def store_activity(activity):
    "Store the activity data in a JSON file"

    try:
        # Get the current date
        date = datetime.now().strftime('%Y-%m-%d')

        # Create the directory for storing the data if it doesn't exist
        os.makedirs(DATA_DIR, exist_ok=True)

        # Define the path to the JSON file
        file_path = os.path.join(DATA_DIR, f'{date}.json')

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

        logger.info(f"Activity stored: {activity}")
    except Exception as e:
        logger.error(f"Error storing activity: {e}")

def store_status_file(filename, content):
    "Store the status file content"
    
    # Create the directory for storing the status files if it doesn't exist
    os.makedirs(STATUS_DIR, exist_ok=True)

    # Define the path to the JSON file
    file_path = os.path.join(STATUS_DIR, f'{filename}.json')

    # Create a dictionary with the file content and timestamp
    status_data = {
        'filename': filename,
        'content': content,
        'timestamp': datetime.now().isoformat()
    }

    # Save the data
    with open(file_path, 'w') as file:
        json.dump(status_data, file, indent=4)

def store_daily_summary(summary):
    "Store the daily summary"
    
    # Create the directory for storing the summaries if it doesn't exist
    os.makedirs(SUMMARIES_DIR, exist_ok=True)

    # Get the current date
    date = datetime.now().strftime('%Y-%m-%d')

    # Define the path to the summary file
    file_path = os.path.join(SUMMARIES_DIR, f'{date}_summary.txt')

    # Save the summary
    with open(file_path, 'w') as file:
        file.write(summary)
