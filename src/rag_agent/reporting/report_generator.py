import json
import os
from datetime import datetime, timedelta

def generate_daily_report(date):
    "Generate a daily report for the given date"

    # Define the path to the JSON file
    file_path = os.path.join('data', f'{date}.json')

    # Load the data
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        return 'No data for the given date'

    # Generate the report
    report = f'Daily Report for {date}:\n'
    for activity in data:
        report += f"{activity['timestamp']}: {activity['category']} - {activity['project']}\n"

    return report

def generate_weekly_report(start_date):
    "Generate a weekly report starting from the given date"

    # Calculate the end date
    end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')

    # Generate the report
    report = f'Weekly Report from {start_date} to {end_date}:\n'
    date = start_date
    while date != end_date:
        report += generate_daily_report(date) + '\n'
        date = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

    return report
