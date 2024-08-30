import time
import os
from datetime import datetime
from src.rag_agent.data_storage.data_store import store_activity, store_status_file
from src.rag_agent.rag_core import process_status_files, generate_daily_summary

import subprocess
import json

def get_active_window_title():
    "Get the active window title"
    
    # This command works on most Linux distributions
    command = 'xdotool getwindowfocus getwindowname'
    window_title = subprocess.check_output(command, shell=True).decode().strip()
    
    return window_title

def categorize_activity(active_window_title):
    "Categorize the activity based on the active window title"
    
    # This is a simple heuristic, you may need to customize it for your needs
    if 'terminal' in active_window_title.lower():
        return 'Coding'
    elif 'word' in active_window_title.lower() or 'docs' in active_window_title.lower():
        return 'Writing'
    else:
        return 'Other'

def associate_activity_with_project(active_window_title):
    "Associate the activity with a project based on the active window title"
    
    # This is a simple heuristic, you may need to customize it for your needs
    if 'rag-agent' in active_window_title.lower():
        return 'RAG Agent Development'
    else:
        return 'Other'

def monitor_activities():
    "Monitor workstation activities and log them"

    while True:
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

        # Wait for a while before checking the active window title again
        time.sleep(1)

def ingest_status_files():
    "Ingest content from status files"
    status_dir = 'status'
    for filename in os.listdir(status_dir):
        file_path = os.path.join(status_dir, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                store_status_file(filename, content)

def generate_end_of_day_summary():
    "Generate and store the end-of-day summary"
    project_summary = process_status_files()
    
    # Load today's activities
    today = datetime.now().strftime('%Y-%m-%d')
    activities_file = f'data/{today}.json'
    if os.path.exists(activities_file):
        with open(activities_file, 'r') as file:
            activities = json.load(file)
    else:
        activities = []
    
    daily_summary = generate_daily_summary(project_summary, activities)
    
    # Save the daily summary
    os.makedirs('data/summaries', exist_ok=True)
    with open(f'data/summaries/{today}_summary.txt', 'w') as file:
        file.write(daily_summary)

if __name__ == "__main__":
    ingest_status_files()
    monitor_activities()
    generate_end_of_day_summary()
