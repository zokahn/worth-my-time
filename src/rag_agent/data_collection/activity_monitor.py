import time
import os
from datetime import datetime

import subprocess

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

        # Log the activity
        print(f"{datetime.now()}: {active_window_title} - {activity_category} - {associated_project}")

        # Wait for a while before checking the active window title again
        time.sleep(1)

if __name__ == "__main__":
    monitor_activities()
