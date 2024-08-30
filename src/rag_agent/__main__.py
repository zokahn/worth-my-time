import os
import subprocess

print("RAG agent started")

# Start the activity monitor in the background
subprocess.Popen(["python", os.path.join("src", "rag_agent", "data_collection", "activity_monitor.py")])
