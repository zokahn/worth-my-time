import time
import os
from datetime import datetime
from src.rag_agent.data_storage.data_store import store_activity, store_status_file
from src.rag_agent.rag_core import process_status_files, generate_daily_summary
from src.rag_agent.utils.logging_config import logger
from src.rag_agent.config import (
    ACTIVITY_MONITOR_INTERVAL, ACTIVITY_CATEGORIES, PROJECT_KEYWORDS,
    STATUS_DIR, DATA_DIR
)

import subprocess
import json

def get_active_window_title():
    "Get the active window title"
    
    try:
        # This command works on most Linux distributions
        command = 'xdotool getwindowfocus getwindowname'
        window_title = subprocess.check_output(command, shell=True).decode().strip()
        return window_title
    except subprocess.CalledProcessError as e:
        logger.error(f"Error getting active window title: {e}")
        return "Unknown"

def categorize_activity(active_window_title):
    "Categorize the activity based on the active window title"
    
    active_window_title = active_window_title.lower()
    for category, keywords in ACTIVITY_CATEGORIES.items():
        if any(keyword in active_window_title for keyword in keywords):
            return category
    return 'Other'

def associate_activity_with_project(active_window_title):
    "Associate the activity with a project based on the active window title"
    
    active_window_title = active_window_title.lower()
    for project, keywords in PROJECT_KEYWORDS.items():
        if any(keyword in active_window_title for keyword in keywords):
            return project
    return 'Other'

def monitor_activities():
    "Monitor workstation activities and log them"

    while True:
        try:
            # Get the active window title
            active_window_title = get_active_window_title()

            # Categorize the activity
            activity_category = categorize_activity(active_window_title)

            # Associate the activity with a project
            associated_project = associate_activity_with_project(active_window_title)

            # Store the activity
            activity = {
                'timestamp': datetime.now().isoformat(),
                'window_title': active_window_title,
                'category': activity_category,
                'project': associated_project
            }
            store_activity(activity)

            logger.info(f"Activity logged: {activity}")

        except Exception as e:
            logger.error(f"Error in monitor_activities: {e}")

        # Wait for a while before checking the active window title again
        time.sleep(ACTIVITY_MONITOR_INTERVAL)

def ingest_status_files():
    "Ingest content from status files"
    try:
        for filename in os.listdir(STATUS_DIR):
            file_path = os.path.join(STATUS_DIR, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                    store_status_file(filename, content)
                    logger.info(f"Ingested status file: {filename}")
    except Exception as e:
        logger.error(f"Error ingesting status files: {e}")

def generate_end_of_day_summary():
    "Generate and store the end-of-day summary"
    project_summary = process_status_files()
    
    # Load today's activities
    today = datetime.now().strftime('%Y-%m-%d')
    activities_file = os.path.join(DATA_DIR, f'{today}.json')
    if os.path.exists(activities_file):
        with open(activities_file, 'r') as file:
            activities = json.load(file)
    else:
        activities = []
    
    daily_summary = generate_daily_summary(project_summary, activities)
    
    # Save the daily summary
    summary_file = os.path.join(DATA_DIR, 'summaries', f'{today}_summary.txt')
    os.makedirs(os.path.dirname(summary_file), exist_ok=True)
    with open(summary_file, 'w') as file:
        file.write(daily_summary)

if __name__ == "__main__":
    ingest_status_files()
    monitor_activities()
    generate_end_of_day_summary()
