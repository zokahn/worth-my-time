import os
import json
from datetime import datetime, timedelta
from src.rag_agent.utils.logging_config import logger
from src.rag_agent.config import STATUS_DIR, DATA_DIR, SUMMARIES_DIR

def process_status_files():
    "Process the ingested status files"
    project_summary = {}
    
    try:
        for filename in os.listdir(STATUS_DIR):
            file_path = os.path.join(STATUS_DIR, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    status_data = json.load(file)
                    file_type = filename.split('.')[0]  # e.g., 'goals', 'decisions_log', etc.
                    
                    # Extract key information based on file type
                    if file_type == 'goals':
                        project_summary['goals'] = extract_goals(status_data['content'])
                    elif file_type == 'decisions_log':
                        project_summary['recent_decisions'] = extract_recent_decisions(status_data['content'])
                    elif file_type == 'open_questions':
                        project_summary['open_questions'] = extract_open_questions(status_data['content'])
                    
                    logger.info(f"Processed status file: {filename}")
    except Exception as e:
        logger.error(f"Error processing status files: {e}")
    
    return project_summary

def extract_goals(content):
    "Extract goals from the content"
    # Simple extraction: assume each line is a goal
    return content.strip().split('\n')

def extract_recent_decisions(content):
    "Extract recent decisions from the content"
    # Simple extraction: take the last 5 lines as recent decisions
    return content.strip().split('\n')[-5:]

def extract_open_questions(content):
    "Extract open questions from the content"
    # Simple extraction: assume each line is a question
    return content.strip().split('\n')

def generate_daily_summary(project_summary, activities):
    "Generate a daily summary based on project status and activities"
    summary = f"Daily Summary for {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    summary += "Project Goals:\n"
    for goal in project_summary.get('goals', []):
        summary += f"- {goal}\n"
    
    summary += "\nRecent Decisions:\n"
    for decision in project_summary.get('recent_decisions', []):
        summary += f"- {decision}\n"
    
    summary += "\nOpen Questions:\n"
    for question in project_summary.get('open_questions', []):
        summary += f"- {question}\n"
    
    summary += "\nToday's Activities:\n"
    activity_categories = {}
    for activity in activities:
        category = activity['category']
        if category not in activity_categories:
            activity_categories[category] = 0
        activity_categories[category] += 1
    
    for category, count in activity_categories.items():
        summary += f"- {category}: {count} activities\n"
    
    return summary

def generate_weekly_summary(start_date):
    "Generate a weekly summary based on daily summaries"
    weekly_summary = f"Weekly Summary for {start_date.strftime('%Y-%m-%d')} to {(start_date + timedelta(days=6)).strftime('%Y-%m-%d')}\n\n"
    
    total_activities = {}
    for i in range(7):
        date = start_date + timedelta(days=i)
        daily_summary_file = os.path.join(SUMMARIES_DIR, f"{date.strftime('%Y-%m-%d')}_summary.txt")
        
        if os.path.exists(daily_summary_file):
            with open(daily_summary_file, 'r') as file:
                daily_summary = file.read()
                
            # Extract activity counts
            activities_section = daily_summary.split("Today's Activities:\n")[-1]
            for line in activities_section.split('\n'):
                if ':' in line:
                    category, count = line.split(':')
                    category = category.strip('- ')
                    count = int(count.split()[0])
                    if category not in total_activities:
                        total_activities[category] = 0
                    total_activities[category] += count
    
    weekly_summary += "Total Activities:\n"
    for category, count in total_activities.items():
        weekly_summary += f"- {category}: {count} activities\n"
    
    return weekly_summary

if __name__ == "__main__":
    project_summary = process_status_files()
    
    # Generate daily summary
    today = datetime.now().strftime('%Y-%m-%d')
    activities_file = os.path.join(DATA_DIR, f'{today}.json')
    if os.path.exists(activities_file):
        with open(activities_file, 'r') as file:
            activities = json.load(file)
    else:
        activities = []
    
    daily_summary = generate_daily_summary(project_summary, activities)
    print(daily_summary)
    
    # Save the daily summary
    summary_file = os.path.join(SUMMARIES_DIR, f'{today}_summary.txt')
    os.makedirs(os.path.dirname(summary_file), exist_ok=True)
    with open(summary_file, 'w') as file:
        file.write(daily_summary)
    
    # Generate weekly summary (if it's the last day of the week)
    if datetime.now().weekday() == 6:  # Sunday
        start_of_week = datetime.now() - timedelta(days=6)
        weekly_summary = generate_weekly_summary(start_of_week)
        print(weekly_summary)
        
        # Save the weekly summary
        weekly_summary_file = os.path.join(SUMMARIES_DIR, f'{start_of_week.strftime("%Y-%m-%d")}_weekly_summary.txt')
        with open(weekly_summary_file, 'w') as file:
            file.write(weekly_summary)
