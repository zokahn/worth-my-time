import ast
import os
from typing import List, Dict
from src.rag_agent.utils.logging_config import logger
from src.rag_agent.notifications.service import notification_service

def analyze_code(file_path: str) -> Dict[str, List[str]]:
    """Analyze a Python file and return a dictionary of suggestions."""
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    suggestions = {
        'complexity': [],
        'naming': [],
        'docstrings': [],
        'imports': []
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check function complexity
            if ast.dump(node).count('ast.') > 20:
                suggestions['complexity'].append(f"Function '{node.name}' might be too complex")

            # Check naming conventions
            if not node.name.islower():
                suggestions['naming'].append(f"Function '{node.name}' should use lowercase with underscores")

            # Check for docstrings
            if not ast.get_docstring(node):
                suggestions['docstrings'].append(f"Function '{node.name}' is missing a docstring")

        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            # Check for unused imports (simplified check)
            for alias in node.names:
                if alias.name not in ast.dump(tree):
                    suggestions['imports'].append(f"Import '{alias.name}' might be unused")

    return suggestions

def review_code(directory: str):
    """Review all Python files in the given directory and its subdirectories."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                suggestions = analyze_code(file_path)
                if any(suggestions.values()):
                    logger.info(f"Code review suggestions for {file_path}:")
                    for category, items in suggestions.items():
                        for item in items:
                            logger.info(f"- {category.capitalize()}: {item}")
                    
                    # Send notification for significant issues
                    if len([item for sublist in suggestions.values() for item in sublist]) > 5:
                        notification_service.send_notification(
                            'system_event',
                            f"Multiple code issues detected in {file_path}. Please review."
                        )

if __name__ == "__main__":
    src_directory = os.path.join(os.path.dirname(__file__), 'src')
    review_code(src_directory)
