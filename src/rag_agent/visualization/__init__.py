import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from datetime import datetime, timedelta
import os

def generate_activity_pie_chart(activities, output_dir):
    """Generate a pie chart of activity categories"""
    categories = Counter(activity['category'] for activity in activities)
    
    plt.figure(figsize=(10, 10))
    plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
    plt.title('Activity Categories')
    
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'activity_categories_pie.png'))
    plt.close()

def generate_activity_timeline(activities, output_dir):
    """Generate a timeline of activities"""
    categories = list(set(activity['category'] for activity in activities))
    colors = plt.cm.rainbow(np.linspace(0, 1, len(categories)))
    color_map = dict(zip(categories, colors))
    
    fig, ax = plt.subplots(figsize=(15, 5))
    
    for activity in activities:
        start_time = datetime.fromisoformat(activity['timestamp'])
        end_time = start_time + timedelta(minutes=5)  # Assume 5-minute duration
        ax.barh(activity['category'], (end_time - start_time).total_seconds() / 3600, 
                left=start_time.hour + start_time.minute / 60, 
                color=color_map[activity['category']], height=0.5)
    
    ax.set_xlim(0, 24)
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Activity Category')
    ax.set_title('Activity Timeline')
    
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'activity_timeline.png'))
    plt.close()
