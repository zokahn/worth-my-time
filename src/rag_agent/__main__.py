import os
import subprocess
import sys
from datetime import datetime, timedelta
from src.rag_agent.reporting import generate_daily_report, generate_weekly_report
from project_assistant import analyze_status_files
from src.rag_agent.rag_core import initialize_plugins
from src.rag_agent.data_collection.activity_monitor import train_models

sys.path.append('.')

print("RAG agent started")

# Initialize plugins
initialize_plugins()

# Train machine learning models
train_models()

# Start the activity monitor in the background
subprocess.Popen(["python", os.path.join("src", "rag_agent", "data_collection", "activity_monitor.py")])

# Initialize the dashboard
from src.rag_agent.dashboard import app as dashboard_app
import threading

dashboard_thread = threading.Thread(target=dashboard_app.run, kwargs={'debug': False, 'use_reloader': False})
dashboard_thread.start()

# Generate and print the daily report for today
print(generate_daily_report(datetime.now().strftime('%Y-%m-%d')))

# Generate and print the weekly report for the past week
print(generate_weekly_report((datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')))

# Analyze the status files and print the insights
print(analyze_status_files())

print("RAG agent, plugins, and dashboard are running")
