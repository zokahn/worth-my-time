import json
import os
from datetime import datetime
from src.rag_agent.utils.logging_config import logger
from src.rag_agent.config import DATA_DIR, STATUS_DIR, SUMMARIES_DIR
from src.rag_agent.utils.exceptions import ActivityStorageError, StatusFileStorageError, SummaryStorageError

def store_activity(activity):
    "Store the activity data in a JSON file"
    try:
        date = datetime.now().strftime('%Y-%m-%d')
        os.makedirs(DATA_DIR, exist_ok=True)
        file_path = os.path.join(DATA_DIR, f'{date}.json')

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(activity)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        logger.info(f"Activity stored: {activity}")
    except Exception as e:
        logger.error(f"Error storing activity: {e}")
        raise ActivityStorageError(f"Failed to store activity: {e}")

def store_status_file(filename, content):
    "Store the status file content"
    try:
        os.makedirs(STATUS_DIR, exist_ok=True)
        file_path = os.path.join(STATUS_DIR, f'{filename}.json')

        status_data = {
            'filename': filename,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }

        with open(file_path, 'w') as file:
            json.dump(status_data, file, indent=4)

        logger.info(f"Status file stored: {filename}")
    except Exception as e:
        logger.error(f"Error storing status file: {e}")
        raise StatusFileStorageError(f"Failed to store status file: {e}")

def store_daily_summary(summary):
    "Store the daily summary"
    try:
        os.makedirs(SUMMARIES_DIR, exist_ok=True)
        date = datetime.now().strftime('%Y-%m-%d')
        file_path = os.path.join(SUMMARIES_DIR, f'{date}_summary.txt')

        with open(file_path, 'w') as file:
            file.write(summary)

        logger.info(f"Daily summary stored for {date}")
    except Exception as e:
        logger.error(f"Error storing daily summary: {e}")
        raise SummaryStorageError(f"Failed to store daily summary: {e}")
