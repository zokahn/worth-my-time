import os
import subprocess
from datetime import datetime, timedelta
from src.rag_agent.reporting import generate_daily_report, generate_weekly_report
from project_assistant import analyze_status_files

print("RAG agent started")

# Start the activity monitor in the background
subprocess.Popen(["python", os.path.join("src", "rag_agent", "data_collection", "activity_monitor.py")])

# Generate and print the daily report for today
print(generate_daily_report(datetime.now().strftime('%Y-%m-%d')))

# Generate and print the weekly report for the past week
print(generate_weekly_report((datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')))

# Analyze the status files and print the insights
print(analyze_status_files())
