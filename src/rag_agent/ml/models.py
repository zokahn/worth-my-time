import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from src.rag_agent.utils.logging_config import logger

class ActivityPredictor:
    def __init__(self):
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000)),
            ('scaler', StandardScaler(with_mean=False)),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])

    def prepare_data(self, activities):
        X = []
        y = []
        for activity in activities:
            features = [
                activity['timestamp'].hour,
                activity['timestamp'].minute,
                activity['timestamp'].weekday(),
                activity['window_title']
            ]
            X.append(features)
            y.append(activity['category'])
        return X, np.array(y)

    def train(self, activities):
        X, y = self.prepare_data(activities)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"Activity Predictor Model Accuracy: {accuracy}")
        logger.info(f"Classification Report:\n{classification_report(y_test, y_pred)}")

    def predict(self, timestamp, window_title):
        features = [[
            timestamp.hour,
            timestamp.minute,
            timestamp.weekday(),
            window_title
        ]]
        return self.model.predict(features)[0]

    def get_feature_importance(self):
        tfidf = self.model.named_steps['tfidf']
        classifier = self.model.named_steps['classifier']
        feature_importance = classifier.feature_importances_
        feature_names = tfidf.get_feature_names_out()
        return sorted(zip(feature_names, feature_importance), key=lambda x: x[1], reverse=True)
