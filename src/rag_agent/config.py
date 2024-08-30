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

# Weekly summary settings
WEEKLY_SUMMARY_DAY = 6  # 0 = Monday, 6 = Sunday
import yaml
from src.rag_agent.config import config

def list_config_settings():
    """List all available configuration settings"""
    for key, value in config.config.items():
        print(f"{key}: {value}")

def generate_sample_config():
    """Generate a sample configuration file"""
    sample_config = {
        'ACTIVITY_MONITOR_INTERVAL': 1,
        'ACTIVITY_CATEGORIES': {
            'Coding': ['terminal', 'code', 'pycharm'],
            'Writing': ['word', 'docs', 'notepad'],
            'Browsing': ['chrome', 'firefox', 'safari'],
        },
        'PROJECT_KEYWORDS': {
            'RAG Agent Development': ['rag-agent', 'rag_agent'],
            'Data Analysis': ['pandas', 'numpy', 'matplotlib'],
        },
        'DATA_DIR': 'data',
        'STATUS_DIR': 'data/status',
        'SUMMARIES_DIR': 'data/summaries',
        'LOG_DIR': 'logs',
        'LOG_LEVEL': 'INFO',
    }

    with open('config.sample.yaml', 'w') as f:
        yaml.dump(sample_config, f, default_flow_style=False)

    print("Sample configuration file 'config.sample.yaml' has been generated.")

def validate_config():
    """Validate the current configuration"""
    try:
        config.validate()
        print("Configuration is valid.")
    except Exception as e:
        print(f"Configuration error: {e}")

if __name__ == "__main__":
    print("RAG Agent Configuration Utilities")
    print("1. List all configuration settings")
    print("2. Generate sample configuration file")
    print("3. Validate current configuration")
    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        list_config_settings()
    elif choice == '2':
        generate_sample_config()
    elif choice == '3':
        validate_config()
    else:
        print("Invalid choice. Please run the script again and select a valid option.")
