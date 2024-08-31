# Installation Guide for RAG Agent

This guide provides detailed instructions for installing and setting up the RAG Agent on your system.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8 or higher
- pip (Python package installer)
- git

## Step-by-Step Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/rag-agent.git
   cd rag-agent
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Unix or MacOS:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Configure the application:
   - Copy the sample configuration file:
     ```
     cp config.sample.yaml config.yaml
     ```
   - Edit `config.yaml` to match your environment and preferences.

6. Set up the database (if applicable):
   ```
   python src/rag_agent/data_storage/setup_db.py
   ```

7. Run the RAG agent:
   ```
   python src/rag_agent/__main__.py
   ```

## Troubleshooting

- If you encounter any "Module not found" errors, ensure that your virtual environment is activated and all dependencies are installed correctly.
- For platform-specific issues:
  - On Linux: Make sure you have `xdotool` installed for window title tracking.
  - On Windows: You may need to install additional packages for window tracking functionality.

## Updating

To update the RAG Agent to the latest version:

1. Stop the running instance of the RAG Agent.
2. Pull the latest changes from the repository:
   ```
   git pull origin main
   ```
3. Activate your virtual environment if it's not already activated.
4. Update dependencies:
   ```
   pip install -r requirements.txt --upgrade
   ```
5. Run any necessary database migrations (if applicable).
6. Restart the RAG Agent.

For any additional help or to report issues, please open an issue on the GitHub repository.
