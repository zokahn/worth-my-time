import os
import json
from datetime import datetime, timedelta
from collections import Counter
from src.rag_agent.utils.logging_config import logger
from src.rag_agent.config import config
from src.rag_agent.notifications.service import notification_service

DATA_DIR = config.get('DATA_DIR')
SUMMARIES_DIR = config.get('SUMMARIES_DIR')
from src.rag_agent.utils.exceptions import StatusFileProcessingError
from src.rag_agent.utils.nlp import categorize_text

def process_status_files():
    "Process the ingested status files"
    project_summary = {}
    
    try:
        for filename in os.listdir(STATUS_DIR):
            file_path = os.path.join(STATUS_DIR, filename)
            if os.path.isfile(file_path):
                try:
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
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding JSON in file {filename}: {e}")
                    notification_service.send_notification('critical_error', f"Error decoding JSON in file {filename}: {e}")
                except KeyError as e:
                    logger.error(f"Missing key in status data for file {filename}: {e}")
                    notification_service.send_notification('critical_error', f"Missing key in status data for file {filename}: {e}")
                except Exception as e:
                    logger.error(f"Unexpected error processing file {filename}: {e}")
                    notification_service.send_notification('critical_error', f"Unexpected error processing file {filename}: {e}")
    except Exception as e:
        logger.error(f"Error accessing status directory: {e}")
        notification_service.send_notification('critical_error', f"Error accessing status directory: {e}")
        raise StatusFileProcessingError(f"Failed to process status files: {e}")
    
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
    "Generate a detailed daily summary based on project status and activities"
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
    activity_categories = Counter()
    project_activities = Counter()
    window_titles = []
    
    for activity in activities:
        activity_categories[activity['category']] += 1
        project_activities[activity['project']] += 1
        window_titles.append(activity['window_title'])
    
    for category, count in activity_categories.items():
        summary += f"- {category}: {count} activities\n"
    
    summary += "\nProject Breakdown:\n"
    for project, count in project_activities.items():
        summary += f"- {project}: {count} activities\n"
    
    summary += "\nMost Common Window Titles:\n"
    for title, count in Counter(window_titles).most_common(5):
        summary += f"- {title}: {count} times\n"
    
    summary += "\nActivity Insights:\n"
    insights = generate_activity_insights(activities)
    summary += insights
    
    summary += "\nRecommendations:\n"
    recommendations = generate_recommendations(insights)
    for recommendation in recommendations:
        summary += f"- {recommendation}\n"
    
    notification_service.send_notification('report_completion', f"Daily summary generated for {datetime.now().strftime('%Y-%m-%d')}")
    
    return summary

def generate_activity_insights(activities):
    "Generate insights from the day's activities"
    insights = ""
    total_activities = len(activities)
    
    if total_activities == 0:
        return "No activities recorded today."
    
    # Time spent on each category
    category_durations = Counter()
    for i in range(len(activities) - 1):
        duration = (datetime.fromisoformat(activities[i+1]['timestamp']) - 
                    datetime.fromisoformat(activities[i]['timestamp'])).total_seconds() / 60
        category_durations[activities[i]['category']] += duration
    
    insights += "Time spent on each category:\n"
    for category, duration in category_durations.most_common():
        insights += f"- {category}: {duration:.2f} minutes\n"
    
    # Most productive hour
    hour_productivity = Counter()
    for activity in activities:
        hour = datetime.fromisoformat(activity['timestamp']).hour
        hour_productivity[hour] += 1
    
    most_productive_hour = hour_productivity.most_common(1)[0]
    insights += f"\nMost productive hour: {most_productive_hour[0]}:00 with {most_productive_hour[1]} activities\n"
    
    # Longest focus period
    longest_focus = max(category_durations.values())
    longest_focus_category = max(category_durations, key=category_durations.get)
    insights += f"\nLongest focus period: {longest_focus:.2f} minutes on {longest_focus_category}\n"
    
    # Task switching frequency
    task_switches = sum(1 for i in range(len(activities) - 1) if activities[i]['category'] != activities[i+1]['category'])
    task_switch_rate = task_switches / (total_activities - 1) if total_activities > 1 else 0
    insights += f"\nTask switching rate: {task_switch_rate:.2f} switches per activity\n"
    
    # Work-life balance
    work_time = sum(duration for category, duration in category_durations.items() if category == 'Coding' or category == 'Writing')
    total_time = sum(category_durations.values())
    work_life_ratio = work_time / total_time if total_time > 0 else 0
    insights += f"\nWork-life balance: {work_life_ratio:.2f} (ratio of work to total activities)\n"
    
    return insights

def generate_recommendations(insights):
    "Generate recommendations based on activity insights"
    recommendations = []
    
    # Parse insights to extract key metrics
    work_life_ratio = float(re.search(r"Work-life balance: ([\d.]+)", insights).group(1))
    task_switch_rate = float(re.search(r"Task switching rate: ([\d.]+)", insights).group(1))
    longest_focus = float(re.search(r"Longest focus period: ([\d.]+)", insights).group(1))
    
    # Work-life balance recommendations
    if work_life_ratio > 0.8:
        recommendations.append("Consider taking more breaks to improve work-life balance.")
    elif work_life_ratio < 0.4:
        recommendations.append("Try to allocate more time for work-related tasks to increase productivity.")
    
    # Task switching recommendations
    if task_switch_rate > 0.5:
        recommendations.append("Your task switching rate is high. Try to group similar tasks together to reduce context switching.")
    
    # Focus recommendations
    if longest_focus < 30:
        recommendations.append("Your longest focus period is relatively short. Consider using techniques like the Pomodoro method to improve focus.")
    
    # Time management recommendation
    recommendations.append("Review your 'Time spent on each category' to identify areas where you might want to reallocate your time.")
    
    return recommendations

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
    
    notification_service.send_notification('report_completion', f"Weekly summary generated for {start_date.strftime('%Y-%m-%d')} to {(start_date + timedelta(days=6)).strftime('%Y-%m-%d')}")
    
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
import os
import yaml
from typing import Dict, Any

class ConfigLoader:
    def __init__(self, config_file='config.yaml'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        env = os.getenv('RAG_AGENT_ENV', 'dev')
        config_file = f'config.{env}.yaml'

        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            # Load user-specific config if it exists
            user_config_file = 'config.user.yaml'
            if os.path.exists(user_config_file):
                with open(user_config_file, 'r') as f:
                    user_config = yaml.safe_load(f)
                config.update(user_config)
            
            return config
        except FileNotFoundError:
            raise ConfigError(f"Configuration file {config_file} not found")
        except yaml.YAMLError as e:
            raise ConfigError(f"Error parsing YAML in {config_file}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def validate(self):
        required_keys = ['ACTIVITY_MONITOR_INTERVAL', 'ACTIVITY_CATEGORIES', 'PROJECT_KEYWORDS', 'DATA_DIR', 'STATUS_DIR', 'SUMMARIES_DIR', 'LOG_DIR', 'LOG_LEVEL']
        for key in required_keys:
            if key not in self.config:
                raise ConfigError(f"Missing required configuration key: {key}")

class ConfigError(Exception):
    pass

# Initialize the global configuration
config = ConfigLoader()
config.validate()

# Export configuration values
ACTIVITY_MONITOR_INTERVAL = config.get('ACTIVITY_MONITOR_INTERVAL')
ACTIVITY_CATEGORIES = config.get('ACTIVITY_CATEGORIES')
PROJECT_KEYWORDS = config.get('PROJECT_KEYWORDS')
DATA_DIR = config.get('DATA_DIR')
STATUS_DIR = config.get('STATUS_DIR')
SUMMARIES_DIR = config.get('SUMMARIES_DIR')
LOG_DIR = config.get('LOG_DIR')
LOG_LEVEL = config.get('LOG_LEVEL')
