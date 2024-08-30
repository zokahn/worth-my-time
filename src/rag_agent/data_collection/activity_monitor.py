import time
import os
from datetime import datetime, timedelta
from src.rag_agent.data_storage import store_activity, store_status_file, store_daily_summary
from src.rag_agent.rag_core import process_status_files, generate_daily_summary, generate_weekly_summary
from src.rag_agent.utils.logging_config import logger
from src.rag_agent.config import config

ACTIVITY_MONITOR_INTERVAL = config.get('ACTIVITY_MONITOR_INTERVAL')
ACTIVITY_CATEGORIES = config.get('ACTIVITY_CATEGORIES')
PROJECT_KEYWORDS = config.get('PROJECT_KEYWORDS')
STATUS_DIR = config.get('STATUS_DIR')
DATA_DIR = config.get('DATA_DIR')
SUMMARIES_DIR = config.get('SUMMARIES_DIR')
from src.rag_agent.utils.exceptions import ActivityMonitorError
from src.rag_agent.utils.nlp import categorize_text

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
    except Exception as e:
        logger.error(f"Unexpected error in get_active_window_title: {e}")
        return "Error"

from src.rag_agent.plugins import plugin_manager
from src.rag_agent.utils.nlp import categorize_text
from src.rag_agent.ml.models import ActivityPredictor, PrivacyClassifier
from src.rag_agent.ml.training import load_activities

activity_predictor = ActivityPredictor()
privacy_classifier = PrivacyClassifier()

def categorize_activity(active_window_title):
    "Categorize the activity based on the active window title using machine learning"
    timestamp = datetime.now()
    category = activity_predictor.predict(timestamp, active_window_title)
    privacy = privacy_classifier.predict(active_window_title)
    return category, privacy

def train_models():
    "Train the activity prediction and privacy classification models"
    activities = load_activities(days=30)  # Load last 30 days of activities
    activity_predictor.train(activities)
    privacy_classifier.train(activities)
    logger.info("Activity prediction and privacy classification models trained")

def associate_activity_with_project(active_window_title):
    "Associate the activity with a project based on the active window title using plugins"
    project_associator_plugin = plugin_manager.get_plugin('project_associator')
    if project_associator_plugin:
        return project_associator_plugin.execute(active_window_title, PROJECT_KEYWORDS)
    return categorize_text(active_window_title, PROJECT_KEYWORDS)

def monitor_activities():
    "Monitor workstation activities and log them"
    while True:
        try:
            active_window_title = get_active_window_title()
            activity_category, privacy = categorize_activity(active_window_title)
            associated_project = associate_activity_with_project(active_window_title)

            activity = {
                'timestamp': datetime.now().isoformat(),
                'window_title': active_window_title,
                'category': activity_category,
                'project': associated_project,
                'privacy': privacy
            }
            store_activity(activity)
            logger.info(f"Activity logged: {activity}")

        except Exception as e:
            logger.error(f"Error in monitor_activities: {e}")
            raise ActivityMonitorError(f"Failed to monitor activities: {e}")

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
        raise ActivityMonitorError(f"Failed to ingest status files: {e}")

def generate_end_of_day_summary():
    "Generate and store the end-of-day summary"
    try:
        project_summary = process_status_files()
        
        today = datetime.now().strftime('%Y-%m-%d')
        activities_file = os.path.join(DATA_DIR, f'{today}.json')
        
        if os.path.exists(activities_file):
            with open(activities_file, 'r') as file:
                activities = json.load(file)
        else:
            activities = []
        
        daily_summary = generate_daily_summary(project_summary, activities)
        store_daily_summary(daily_summary)
        
        if datetime.now().weekday() == 6:  # Sunday
            start_of_week = datetime.now() - timedelta(days=6)
            weekly_summary = generate_weekly_summary(start_of_week)
            weekly_summary_file = os.path.join(SUMMARIES_DIR, f'{start_of_week.strftime("%Y-%m-%d")}_weekly_summary.txt')
            with open(weekly_summary_file, 'w') as file:
                file.write(weekly_summary)
            logger.info(f"Weekly summary generated and stored: {weekly_summary_file}")
    
    except Exception as e:
        logger.error(f"Error generating end-of-day summary: {e}")
        raise ActivityMonitorError(f"Failed to generate end-of-day summary: {e}")

from src.rag_agent.dashboard import app as dashboard_app
import threading

if __name__ == "__main__":
    try:
        # Start the dashboard in a separate thread
        dashboard_thread = threading.Thread(target=dashboard_app.run, kwargs={'debug': False, 'use_reloader': False})
        dashboard_thread.start()
        
        ingest_status_files()
        monitor_activities()
        
        # Generate end-of-day summary
        generate_end_of_day_summary()
        
        logger.info("RAG Agent and dashboard are running")
    
    except Exception as e:
        logger.critical(f"Critical error in main execution: {e}")
    
    finally:
        # Ensure the dashboard thread is properly terminated
        if 'dashboard_thread' in locals() and dashboard_thread.is_alive():
            dashboard_thread.join()
