import requests
from github import Github, GithubException
import socket
import os
import platform
import json

def update_counter():
    # Hardcoded GitHub credentials and repository details
    token = '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'  # Your GitHub token
    repo_name = 'randumduck/script-counter'  # Your repository name
    file_path = 'counter.json'  # Path to the counter file in your repository

    # Get the external IP address and OS name
    ip_address = requests.get('https://api.ipify.org').text
    os_name = platform.system()
    hostname = socket.gethostname()
    script_name = os.path.basename(__file__)

    # Authenticate to GitHub and get the repository
    repo = Github(token).get_repo(repo_name)

    # Get the current counter data and update it
    try:
        file = repo.get_contents(file_path)
        counter_data = json.loads(file.decoded_content.decode())
        sha = file.sha  # Store the SHA of the file for updating
    except GithubException as e:
        if e.status == 404:
            counter_data = []
            sha = None  # No existing file, so no SHA
        else:
            raise e

    # Find the script entry or create a new one
    script_entry = next((entry for entry in counter_data if entry['script_name'] == script_name), None)
    if script_entry:
        script_entry['count'] += 1
        script_entry['details'].append({
            'os_name': os_name,
            'hostname': hostname,
            'ip_address': ip_address
        })
    else:
        script_entry = {
            'serial_number': len(counter_data) + 1,
            'script_name': script_name,
            'count': 1,
            'details': [{
                'os_name': os_name,
                'hostname': hostname,
                'ip_address': ip_address
            }]
        }
        counter_data.append(script_entry)

    # Update or create the counter file in the repository without changing the web page
    if sha:
        repo.update_file(file_path, "Update counter data", json.dumps(counter_data), sha)
    else:
        repo.create_file(file_path, "Create counter data", json.dumps(counter_data))

# Call the function to update the counter
if __name__ == "__main__":
    update_counter()
