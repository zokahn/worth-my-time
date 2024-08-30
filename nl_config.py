import yaml
from src.rag_agent.config import config
import re
from src.rag_agent.utils.logging_config import logger

def parse_natural_language_config(nl_config: str) -> dict:
    """Parse natural language configuration and return a dictionary."""
    parsed_config = {}
    
    # Example parsing rules (extend as needed)
    if re.search(r'monitor activities every (\d+) seconds', nl_config, re.IGNORECASE):
        interval = re.search(r'monitor activities every (\d+) seconds', nl_config, re.IGNORECASE).group(1)
        parsed_config['ACTIVITY_MONITOR_INTERVAL'] = int(interval)
    
    if re.search(r'log level should be (DEBUG|INFO|WARNING|ERROR|CRITICAL)', nl_config, re.IGNORECASE):
        log_level = re.search(r'log level should be (DEBUG|INFO|WARNING|ERROR|CRITICAL)', nl_config, re.IGNORECASE).group(1)
        parsed_config['LOG_LEVEL'] = log_level.upper()
    
    # Add more parsing rules here
    
    return parsed_config

def update_config_from_nl(nl_config: str):
    """Update the configuration based on natural language input."""
    parsed_config = parse_natural_language_config(nl_config)
    
    for key, value in parsed_config.items():
        config.config[key] = value
        logger.info(f"Updated configuration: {key} = {value}")
    
    # Save the updated configuration
    with open('config.yaml', 'w') as f:
        yaml.dump(config.config, f, default_flow_style=False)
    
    logger.info("Configuration updated and saved.")

if __name__ == "__main__":
    nl_input = input("Enter your configuration in natural language: ")
    update_config_from_nl(nl_input)
