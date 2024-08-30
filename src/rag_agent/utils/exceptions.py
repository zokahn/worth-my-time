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
