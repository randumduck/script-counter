import requests
from github import Github

# GitHub credentials
token = 'your_github_token'
repo_name = 'your_username/script-counter'
file_path = 'counter.txt'

# Authenticate to GitHub
g = Github(token)
repo = g.get_repo(repo_name)

# Get the current counter value
file = repo.get_contents(file_path)
counter = int(file.decoded_content.decode()) + 1

# Update the counter value
repo.update_file(file_path, 'Update counter', str(counter), file.sha)
