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

if __name__ == "__main__":
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
    print(daily_summary)
    
    # Save the daily summary
    summary_file = os.path.join(SUMMARIES_DIR, f'{today}_summary.txt')
    os.makedirs(os.path.dirname(summary_file), exist_ok=True)
    with open(summary_file, 'w') as file:
        file.write(daily_summary)
