import requests
import json
import os
from git import Repo
from datetime import datetime

# Configuration
API_URL = "https://romanapi.fly.dev/api/anime"  # Replace with the actual API URL
LOCAL_FILE = "export.json"
REPO_PATH = os.path.dirname(os.path.abspath(__file__))  # Path to the repo (assumes this script is in the repo folder)
COMMIT_MESSAGE = "Auto-update export.json with latest anime data"

def fetch_data_from_api():
    """Fetches the data from the API."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def save_data_to_file(data):
    """Saves the data to export.json if it has changed."""
    if os.path.exists(LOCAL_FILE):
        with open(LOCAL_FILE, 'r') as file:
            existing_data = json.load(file)
        if data == existing_data:
            print("No changes detected in the data. Skipping save.")
            return False

    # Save new data
    with open(LOCAL_FILE, 'w') as file:
        json.dump(data, file, indent=4)
    print("Data saved to export.json")
    return True

def commit_and_push_changes():
    """Commits and pushes changes to the GitHub repository."""
    try:
        repo = Repo(REPO_PATH)
        repo.git.add(LOCAL_FILE)
        if repo.is_dirty():
            repo.index.commit(f"{COMMIT_MESSAGE} ({datetime.now().isoformat()})")
            origin = repo.remote(name='origin')
            origin.push()
            print("Changes committed and pushed to GitHub.")
        else:
            print("No changes to commit.")
    except Exception as e:
        print(f"Error during Git operations: {e}")

def main():
    """Main script to fetch, save, and push updates."""
    print("Starting data synchronization...")
    data = fetch_data_from_api()
    if data is not None:
        if save_data_to_file(data):
            commit_and_push_changes()
    print("Data synchronization complete.")

if __name__ == "__main__":
    main()
