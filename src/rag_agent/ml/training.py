import json
from datetime import datetime, timedelta
from src.rag_agent.config import DATA_DIR
from src.rag_agent.ml.models import ActivityPredictor
from src.rag_agent.utils.logging_config import logger
import os

def load_activities(days=30):
    activities = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        file_path = os.path.join(DATA_DIR, f'{date}.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                daily_activities = json.load(f)
                for activity in daily_activities:
                    activity['timestamp'] = datetime.fromisoformat(activity['timestamp'])
                activities.extend(daily_activities)
    return activities

def train_activity_predictor():
    activities = load_activities()
    if not activities:
        logger.warning("No activities found for training")
        return

    predictor = ActivityPredictor()
    predictor.train(activities)
    return predictor

if __name__ == "__main__":
    trained_model = train_activity_predictor()
    # Here you could save the trained model for later use
