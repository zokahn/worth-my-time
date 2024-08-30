import os
import json

def process_status_files():
    "Process the ingested status files"
    status_dir = 'data/status'
    for filename in os.listdir(status_dir):
        file_path = os.path.join(status_dir, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                status_data = json.load(file)
                # Process the status data here
                # This is where you would implement your RAG logic
                print(f"Processing status file: {status_data['filename']}")
                print(f"Content: {status_data['content'][:100]}...")  # Print first 100 characters

if __name__ == "__main__":
    process_status_files()
