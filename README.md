# script-counter
A webpage on GitHub that has a counter which increments every time your script runs.
Sure! Here’s a detailed step-by-step guide for your `README.md` file to help you set up and run the script that updates the counter on your GitHub repository.

### README.md

```markdown
# Script Run Counter

This project tracks the execution of scripts and updates a counter on a GitHub repository. The counter is displayed on a webpage in a tabular format, showing the script name, the number of times it has run, and details about the machine it ran on.

## Prerequisites

- Python 3.x
- GitHub account
- GitHub Personal Access Token with `repo` scope
- `requests` and `PyGithub` Python libraries

## Setup

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/your_username/script-counter.git
cd script-counter
```

### 2. Install Required Python Libraries

Install the required Python libraries using pip:

```bash
pip install requests PyGithub
```

### 3. Create `counter.json` File

If `counter.json` does not exist in the repository, create it manually with the following content:

```json
[]
```

### 4. Update the Python Script

Ensure the Python script (`script-counter.py`) is updated with your GitHub token and repository details:

```python
import requests
from github import Github, GithubException
import socket
import os
import platform
import json

def update_counter():
    # Hardcoded GitHub credentials and repository details
    token = 'your_github_token'  # Your GitHub token
    repo_name = 'your_username/script-counter'  # Your repository name
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
```

### 5. Create or Update `index.html`

Ensure the `index.html` file is present in the repository with the following content to display the counter:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Script Run Counter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Script Run Counter</h1>
    <table>
        <thead>
            <tr>
                <th>Serial Number</th>
                <th>Script Name</th>
                <th>Number of Times Ran</th>
                <th>Details (OS Type, Hostname, IP Address)</th>
            </tr>
        </thead>
        <tbody id="counter-table">
            <!-- Data will be inserted here by JavaScript -->
        </tbody>
    </table>

    <script>
        fetch('https://raw.githubusercontent.com/your_username/script-counter/main/counter.json')
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById('counter-table');
                data.forEach(entry => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${entry.serial_number}</td>
                        <td>${entry.script_name}</td>
                        <td>${entry.count}</td>
                        <td>${entry.details.map(detail => `${detail.os_name}, ${detail.hostname}, ${detail.ip_address}`).join('<br>')}</td>
                    `;
                    tableBody.appendChild(row);
                });
            });
    </script>
</body>
</html>
```

### 6. Run the Script

Run the Python script to update the counter:

```bash
python3 script-counter.py
```

You can also rename the script and run it to see the counter update for different script names:

```bash
cp script-counter.py scc.py
python3 scc.py
```

### 7. View the Webpage

Visit your GitHub Pages site to view the updated counter:

```
https://your_username.github.io/script-counter/
```

### Troubleshooting

- Ensure your GitHub token has the `repo` scope.
- Verify the repository name and file paths are correct.
- Check for any errors in the console or logs.
