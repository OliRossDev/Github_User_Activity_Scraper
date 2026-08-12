import sys
import urllib.request
import json

#Check to see if the username is entered into the terminal
if len(sys.argv) < 2:
    print("Username not found/inputted. Please try again.");
    sys.exit();

#Get the inputted username and add into the URL to fetch events from the Github API. 
# If it fails, display an error message
username = sys.argv[1]
url = f"https://api.github.com/users/{username}/events"

try:
    with urllib.request.urlopen(url) as response:
        data_string = response.read().decode("utf-8")
        events_data = json.loads(data_string)
except Exception as e:
    print(f"Error fetching events: {e}")
    sys.exit()

#Check to see if the events data has any events, if it does, display the event type and the repo name.

for event in events_data:
    event_type = event.get("type", "N/A")
    repo_info = event.get("repo", "N/A")
    repo_name = repo_info.get("name", "unknown repo")

    if event_type == "PushEvent":
        payload = event.get("payload", {})
        commits = payload.get("commits", [])

        if len(commits) > 0:
            commit_count = len(commits)
            print(f"- Pushed {commit_count} commits to {repo_name}")
    elif event_type == "IssuesEvent":
        payload = event.get("payload", {})
        action = payload.get("action", "unknown ")
        print(f"- {action.capitalize()} an issue in {repo_name}")
    else:
        print(f"- {event_type} in {repo_name}")