class RAGAgentError(Exception):
    """Base exception class for RAG Agent"""
    pass

class ActivityMonitorError(RAGAgentError):
    """Exception raised for errors in the activity monitoring process"""
    pass

class StatusFileProcessingError(RAGAgentError):
    """Exception raised for errors in processing status files"""
    pass

class ActivityStorageError(RAGAgentError):
    """Exception raised for errors in storing activity data"""
    pass

class StatusFileStorageError(RAGAgentError):
    """Exception raised for errors in storing status files"""
    pass

class SummaryStorageError(RAGAgentError):
    """Exception raised for errors in storing summary data"""
    pass
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def categorize_text(text, categories, training_data=None):
    """
    Categorize text using TF-IDF and Naive Bayes if training data is provided,
    otherwise fall back to keyword matching.
    
    :param text: The text to categorize
    :param categories: A dictionary of categories and their associated keywords
    :param training_data: A list of (text, category) tuples for training
    :return: The most likely category
    """
    if training_data:
        # Use machine learning approach
        texts, labels = zip(*training_data)
        classifier = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', MultinomialNB()),
        ])
        classifier.fit(texts, labels)
        return classifier.predict([text])[0]
    else:
        # Fall back to keyword matching
        word_counts = Counter(re.findall(r'\w+', text.lower()))
        category_scores = {category: sum(word_counts[keyword.lower()] for keyword in keywords)
                           for category, keywords in categories.items()}
        return max(category_scores, key=category_scores.get)
