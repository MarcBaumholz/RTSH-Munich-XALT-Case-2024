import requests
import csv
import pandas as pd
from requests.auth import HTTPBasicAuth
import yaml
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
    jira_api_token = config["jira"]["api_token"]
    confluence_email = config["jira"]["credentials"]["email"]
    openai_api_token = config["openai"]["api_token"]
    confluence_api_token = config["jira"]["api_token"]
# Confluence API Details



#confluence_url = "https://one-atlas-nicz.atlassian.net/wiki/rest/api/content"

#TODO only project 1 done
base_url = config.get("project1", {}).get("url", "")  # Assuming 'project1.url' contains the Jira URL

# Extract the base URL (everything before '/jira')
jira_url = base_url.split("jira")[0]
confluence_url = f"{jira_url}wiki/rest/api/content"

print(confluence_url)

space_key = "EO"  # Replace with your Confluence space key
parent_page_id = 3538975  #Replace with the parent page ID (if needed)

# Load AI summary from CSV using pandas
csv_file_path = "./data/ai_summary.csv"  # Replace with the path to your CSV file
df = pd.read_csv(csv_file_path)
ai_summary = df['summary_text'].iloc[0]  # Assuming the summary is in the 'txt' column of the first row

title = " ".join(ai_summary.split()[:2])
# Prepare the Confluence page payload
confluence_payload = {
    "type": "page",
    "title": title,
    "space": {
        "key": space_key
    },
    "body": {
        "storage": {
            "value": f"<h1>Summary</h1><p>{ai_summary}</p>",
            "representation": "storage"
        }
    }
}
if parent_page_id:
    confluence_payload["ancestors"] = [{"id": parent_page_id}]

confluence_headers = {
    "Authorization": f"Bearer {confluence_api_token}",
    "Content-Type": "application/json"
}

"""
# Headers for Confluence request


# Push the summary to Confluence
response = requests.post(confluence_url, json=confluence_payload, headers=confluence_headers)
"""
# Make the API request
response = requests.post(
    confluence_url,
    headers=confluence_headers,
    json=confluence_payload,
    auth=HTTPBasicAuth(confluence_email, confluence_api_token)  # Basic Auth using email and token
)

# Handle response
if response.status_code in (200, 201):
    print("Confluence page successfully created!")
    page_data = response.json()
    print(f"View it here: {page_data['_links']['base']}{page_data['_links']['webui']}")
else:
    print(f"Failed to create Confluence page. HTTP Status Code: {response.status_code}")
    print(response.text)
