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

def categorize_text(text, categories):
    """
    Categorize text based on keyword matching.
    
    :param text: The text to categorize
    :param categories: A dictionary of categories and their associated keywords
    :return: The most likely category
    """
    word_counts = Counter(re.findall(r'\w+', text.lower()))
    category_scores = {category: sum(word_counts[keyword.lower()] for keyword in keywords)
                       for category, keywords in categories.items()}
    return max(category_scores, key=category_scores.get)
