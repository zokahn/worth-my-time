import time
import os
from datetime import datetime

def monitor_activities():
    "Monitor workstation activities and log them"

    # TODO: Implement the logic to track the active window title and categorize the activity

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
