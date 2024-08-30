import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from src.rag_agent.utils.logging_config import logger

class ActivityPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def prepare_data(self, activities):
        X = []
        y = []
        for activity in activities:
            features = [
                activity['timestamp'].hour,
                activity['timestamp'].minute,
                activity['timestamp'].weekday(),
                hash(activity['window_title']) % 1000  # Simple feature hashing
            ]
            X.append(features)
            y.append(activity['category'])
        return np.array(X), np.array(y)

    def train(self, activities):
        X, y = self.prepare_data(activities)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"Activity Predictor Model Accuracy: {accuracy}")
        logger.info(f"Classification Report:\n{classification_report(y_test, y_pred)}")

    def predict(self, timestamp, window_title):
        features = np.array([[
            timestamp.hour,
            timestamp.minute,
            timestamp.weekday(),
            hash(window_title) % 1000
        ]])
        return self.model.predict(features)[0]
