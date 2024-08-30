import json
from datetime import datetime, timedelta
from src.rag_agent.config import DATA_DIR
from src.rag_agent.ml.models import ActivityPredictor
from src.rag_agent.utils.logging_config import logger
import os
import joblib

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
        return None

    predictor = ActivityPredictor()
    predictor.train(activities)
    return predictor

def save_model(model, filename='activity_predictor.joblib'):
    joblib.dump(model, filename)
    logger.info(f"Model saved to {filename}")

def load_model(filename='activity_predictor.joblib'):
    model = joblib.load(filename)
    logger.info(f"Model loaded from {filename}")
    return model

def analyze_feature_importance(model):
    feature_importance = model.get_feature_importance()
    logger.info("Top 10 most important features:")
    for feature, importance in feature_importance[:10]:
        logger.info(f"{feature}: {importance}")

def evaluate_model(model, test_activities):
    X_test, y_test = model.prepare_data(test_activities)
    y_pred = model.model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Model Accuracy on Test Set: {accuracy}")
    logger.info(f"Classification Report:\n{classification_report(y_test, y_pred)}")

if __name__ == "__main__":
    trained_model = train_activity_predictor()
    if trained_model:
        save_model(trained_model)
        analyze_feature_importance(trained_model)
        
        # Evaluate the model on a separate test set
        test_activities = load_activities(days=7)  # Use the last 7 days as a test set
        evaluate_model(trained_model, test_activities)
