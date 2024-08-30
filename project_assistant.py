import os
import json
from datetime import datetime
from src.rag_agent.utils.logging_config import logger
from src.rag_agent.notifications.service import notification_service
from src.rag_agent.utils.nlp import categorize_text

def analyze_status_files():
    """Analyze status files and provide insights"""
    status_dir = 'status'
    insights = {}

    for file_name in os.listdir(status_dir):
        if file_name.endswith(('.txt', '.md')):
            file_path = os.path.join(status_dir, file_name)
            with open(file_path, 'r') as file:
                content = file.read()
            insights[file_name] = analyze_status_file(content)

    return insights

def analyze_status_file(content):
    """Analyze a status file and provide insights"""
    insights = {
        'word_count': len(content.split()),
        'line_count': len(content.splitlines()),
        'sentiment': analyze_sentiment(content),
        'key_topics': extract_key_topics(content),
        'action_items': extract_action_items(content)
    }
    return insights

def analyze_sentiment(text):
    """Placeholder for sentiment analysis"""
    # TODO: Implement actual sentiment analysis
    return "neutral"

def extract_key_topics(text):
    """Extract key topics from the text"""
    # TODO: Implement more sophisticated topic extraction
    words = text.lower().split()
    return [word for word in set(words) if len(word) > 5][:5]

def extract_action_items(text):
    """Extract action items from the text"""
    action_items = []
    for line in text.splitlines():
        if line.strip().lower().startswith(('todo', 'to-do', 'action item')):
            action_items.append(line.strip())
    return action_items

def generate_project_summary():
    """Generate a summary of the project status"""
    insights = analyze_status_files()
    summary = f"Project Summary as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    for file, file_insights in insights.items():
        summary += f"File: {file}\n"
        summary += f"Word count: {file_insights['word_count']}\n"
        summary += f"Line count: {file_insights['line_count']}\n"
        summary += f"Sentiment: {file_insights['sentiment']}\n"
        summary += f"Key topics: {', '.join(file_insights['key_topics'])}\n"
        if file_insights['action_items']:
            summary += "Action items:\n"
            for item in file_insights['action_items']:
                summary += f"- {item}\n"
        summary += "\n"

    logger.info("Generated project summary")
    notification_service.send_notification('system_event', "New project summary available")
    return summary

if __name__ == "__main__":
    summary = generate_project_summary()
    print(summary)
    
    # Save the summary
    with open('project_summary.txt', 'w') as f:
        f.write(summary)
