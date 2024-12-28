import requests
from github import Github, GithubException
import socket, os, platform, json

def update_counter():
    token, repo_name, file_path = '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', 'randumduck/script-counter', 'counter.json'
    ip_address, os_name, hostname, script_name = requests.get('https://api.ipify.org').text, platform.system(), socket.gethostname(), os.path.basename(__file__)
    repo = Github(token).get_repo(repo_name)

    try:
        file = repo.get_contents(file_path)
        counter_data, sha = json.loads(file.decoded_content.decode()), file.sha
    except GithubException as e:
        if e.status == 404:
            counter_data, sha = [], None
        else:
            raise e

    script_entry = next((entry for entry in counter_data if entry['script_name'] == script_name), None)
    if script_entry:
        script_entry['count'] += 1
        script_entry['details'].append({'os_name': os_name, 'hostname': hostname, 'ip_address': ip_address})
    else:
        counter_data.append({
            'serial_number': len(counter_data) + 1,
            'script_name': script_name,
            'count': 1,
            'details': [{'os_name': os_name, 'hostname': hostname, 'ip_address': ip_address}]
        })

    if sha:
        repo.update_file(file_path, "Update counter data", json.dumps(counter_data), sha)
    else:
        repo.create_file(file_path, "Create counter data", json.dumps(counter_data))

if __name__ == "__main__":
    update_counter()
