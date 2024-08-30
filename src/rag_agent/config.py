# Configuration settings for the RAG Agent

# Activity monitoring settings
ACTIVITY_MONITOR_INTERVAL = 1  # seconds

# Activity categorization settings
ACTIVITY_CATEGORIES = {
    'Coding': ['terminal', 'code', 'pycharm', 'intellij', 'vim', 'emacs'],
    'Writing': ['word', 'docs', 'notepad', 'textedit'],
    'Browsing': ['chrome', 'firefox', 'safari', 'edge'],
    'Communication': ['slack', 'teams', 'zoom', 'skype'],
    'Design': ['photoshop', 'illustrator', 'figma', 'sketch'],
}

# Project association settings
PROJECT_KEYWORDS = {
    'RAG Agent Development': ['rag-agent', 'rag_agent', 'ragagent'],
    'Data Analysis': ['pandas', 'numpy', 'matplotlib', 'jupyter'],
    'Web Development': ['django', 'flask', 'react', 'vue', 'angular'],
}

# Data storage settings
DATA_DIR = 'data'
STATUS_DIR = 'data/status'
SUMMARIES_DIR = 'data/summaries'

# Logging settings
LOG_DIR = 'logs'
LOG_LEVEL = 'INFO'
