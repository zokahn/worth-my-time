import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from src.rag_agent.utils.logging_config import logger
import joblib

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
        self.activities = activities  # Store activities for later use
        X, y = self.prepare_data(activities)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"Activity Predictor Model Accuracy: {accuracy}")
        logger.info(f"Classification Report:\n{classification_report(y_test, y_pred)}")
        
        # Perform cross-validation
        cv_scores = cross_val_score(self.model, X, y, cv=5)
        logger.info(f"Cross-validation scores: {cv_scores}")
        logger.info(f"Mean CV score: {np.mean(cv_scores):.2f} (+/- {np.std(cv_scores) * 2:.2f})")

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

    def predict_proba(self, timestamp, window_title):
        features = [[
            timestamp.hour,
            timestamp.minute,
            timestamp.weekday(),
            window_title
        ]]
        return self.model.predict_proba(features)[0]

    def get_top_features(self, n=10):
        feature_importance = self.get_feature_importance()
        return feature_importance[:n]

    def get_model_performance(self):
        X, y = self.prepare_data(self.activities)
        X_test, y_test = X[-len(X)//5:], y[-len(y)//5:]  # Use last 20% as test set
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        conf_matrix = confusion_matrix(y_test, y_pred)
        return accuracy, f1, conf_matrix

    def visualize_feature_importance(self, n=20):
        feature_importance = self.get_feature_importance()
        top_n = feature_importance[:n]
        features, importance = zip(*top_n)
        
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(features)), importance)
        plt.xticks(range(len(features)), features, rotation=90)
        plt.xlabel('Features')
        plt.ylabel('Importance')
        plt.title(f'Top {n} Feature Importance')
        plt.tight_layout()
        plt.savefig('feature_importance.png')
        logger.info(f"Feature importance visualization saved as 'feature_importance.png'")

    def save_model(self, filename='activity_predictor_model.joblib'):
        joblib.dump(self.model, filename)
        logger.info(f"Model saved to {filename}")

    def load_model(self, filename='activity_predictor_model.joblib'):
        self.model = joblib.load(filename)
        logger.info(f"Model loaded from {filename}")

class PrivacyClassifier:
    def __init__(self):
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=500)),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])

    def train(self, activities):
        X = [activity['window_title'] for activity in activities]
        y = [activity.get('privacy', 'unknown') for activity in activities]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"Privacy Classifier Model Accuracy: {accuracy}")
        logger.info(f"Classification Report:\n{classification_report(y_test, y_pred)}")

    def predict(self, window_title):
        return self.model.predict([window_title])[0]

    def predict_proba(self, window_title):
        return self.model.predict_proba([window_title])[0]

    def get_feature_importance(self):
        tfidf = self.model.named_steps['tfidf']
        classifier = self.model.named_steps['classifier']
        feature_importance = classifier.feature_importances_
        feature_names = tfidf.get_feature_names_out()
        return sorted(zip(feature_names, feature_importance), key=lambda x: x[1], reverse=True)

    def get_top_features(self, n=10):
        feature_importance = self.get_feature_importance()
        return feature_importance[:n]
