import requests
from requests.auth import HTTPBasicAuth
import yaml
import pandas as pd
# Load the API token from config.yaml
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
    api_token = config["jira"]["api_token"]
    email = config["jira"]["credentials"]["email"]

#
#TODO: only for project1 done 

# Jira Cloud URL and credentials
jira_url = config.get("project1", {}).get("url", "")  # Assuming 'project1.url' contains the Jira URL
# Extract the base URL (everything before '/jira')
base_url = jira_url.split("jira")[0]

# Extract the project name (the part after '/projects/')
project_name = jira_url.split("/projects/")[1].split("/")[0]


api_endpoint = f"{base_url}/rest/api/3/field"
endpoint_project = f"{base_url}/rest/api/3/project"

print(base_url)
print(project_name)
# Get the jira_url from the config

headers = {
    "Accept": "application/json"
}

# Making the GET request
response = requests.get(api_endpoint, headers=headers, auth=HTTPBasicAuth(email, api_token))

if response.status_code == 200:
    fields = response.json()
    # Filter custom fields
    custom_fields = [field for field in fields if "schema" in field and "custom" in field["schema"]]

    # Extract specific custom fields
    field_mapping = {
        "epiclink": next(field["id"] for field in custom_fields if field["name"] == "Epic Link"),
        "epicname": next(field["id"] for field in custom_fields if field["name"] == "Epic Name"),
        "epicstatus": next(field["id"] for field in custom_fields if field["name"] == "Epic Status")
    }

    print("Custom Field Mapping:", field_mapping)

else:
    print(f"Failed to fetch fields. Status Code: {response.status_code}")
    print(response.text)

# Making the GET request
response2 = requests.get(endpoint_project, headers=headers, auth=HTTPBasicAuth(email, api_token))

if response2.status_code == 200:
    projects = response2.json()
    # Filter projects with "DESIGN" in the name
    design_projects = [project for project in projects if project_name in project['key']]
    if design_projects:
        for project in design_projects:
            print(f"Design Project Name: {project['name']}, Project Key: {project['key']}")
            project_key = project['key'] 
    else:
        for project in projects:
            print(f"Project Name: {project['name']}, Project Key: {project['key']}")
else:
    print(f"Failed to fetch projects. Status Code: {response2.status_code}")
    print(response2.text)

"""
# API endpoint to retrieve statuses
statuses_endpoint = f"{base_url}/rest/api/3/status"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Making the GET request
response3 = requests.get(statuses_endpoint, headers=headers, auth=HTTPBasicAuth(email, api_token))

if response3.status_code == 200:
    statuses = response3.json()

    print("Status-IDs and their names:")
    for status in statuses:
        print(f"ID: {status['id']}, Name: {status['name']}")
else:
    print(f"Failed to retrieve statuses. Status Code: {response3.status_code}")
    print(response3.text)

# Ticket key (replace with an actual issue key in your project)
issue_key = "DESIGN-1"  # Beispiel-Ticket

# API endpoint to retrieve transitions for a specific issue
transitions_endpoint = f"{base_url}/rest/api/3/issue/{issue_key}/transitions"

# Making the GET request
response4 = requests.get(transitions_endpoint, headers=headers, auth=HTTPBasicAuth(email, api_token))

if response4.status_code == 200:
    transitions = response4.json()["transitions"]

    print("Available Transitions for the Issue:")
    for transition in transitions:
        print(f"ID: {transition['id']}, Name: {transition['name']}")
else:
    print(f"Failed to retrieve transitions. Status Code: {response4.status_code}")
    print(response4.text)
"""
data = {
    "epiclink": field_mapping.get("epiclink", ""),
    "epicname": field_mapping.get("epicname", ""),
    "epicstatus": field_mapping.get("epicstatus", ""),
    "project_keys": project_key
}
df = pd.DataFrame([data])  # Creating a DataFrame
df.to_csv("./data/jira_data.csv", index=False)  # Saving to CSV
print("Data saved to jira_data.csv")