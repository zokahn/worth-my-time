import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from src.rag_agent.config import DATA_DIR, SUMMARIES_DIR
from src.rag_agent.utils.logging_config import logger

def load_activity_data(days=7):
    """Load activity data for the specified number of days"""
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days-1)
    current_date = start_date

    while current_date <= end_date:
        file_path = os.path.join(DATA_DIR, f"{current_date.strftime('%Y-%m-%d')}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                daily_data = json.load(f)
                data.extend(daily_data)
        current_date += timedelta(days=1)

    return pd.DataFrame(data)

def visualize_activity_distribution(df):
    """Visualize the distribution of activities"""
    plt.figure(figsize=(12, 6))
    sns.countplot(y='category', data=df, order=df['category'].value_counts().index)
    plt.title('Distribution of Activities')
    plt.xlabel('Count')
    plt.ylabel('Activity Category')
    plt.tight_layout()
    plt.savefig(os.path.join(SUMMARIES_DIR, 'activity_distribution.png'))
    plt.close()

def visualize_activity_timeline(df):
    """Visualize the timeline of activities"""
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    activity_counts = df.groupby(['date', 'category']).size().unstack(fill_value=0)

    plt.figure(figsize=(12, 6))
    activity_counts.plot(kind='area', stacked=True)
    plt.title('Activity Timeline')
    plt.xlabel('Date')
    plt.ylabel('Number of Activities')
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(SUMMARIES_DIR, 'activity_timeline.png'))
    plt.close()

def visualize_project_distribution(df):
    """Visualize the distribution of activities across projects"""
    plt.figure(figsize=(12, 6))
    sns.countplot(y='project', data=df, order=df['project'].value_counts().index)
    plt.title('Distribution of Activities Across Projects')
    plt.xlabel('Count')
    plt.ylabel('Project')
    plt.tight_layout()
    plt.savefig(os.path.join(SUMMARIES_DIR, 'project_distribution.png'))
    plt.close()

def generate_visualizations():
    """Generate all visualizations"""
    df = load_activity_data()
    
    visualize_activity_distribution(df)
    visualize_activity_timeline(df)
    visualize_project_distribution(df)
    
    logger.info("Generated visualizations")

if __name__ == "__main__":
    generate_visualizations()
