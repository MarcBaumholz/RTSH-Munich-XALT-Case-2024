import requests
from requests.auth import HTTPBasicAuth

# Jira Cloud URL and credentials
jira_url = "https://one-atlas-nicz.atlassian.net/"
ticket_key = "DESIGN-2"  # Replace with your ticket key
api_endpoint = f"{jira_url}/rest/api/3/issue/{ticket_key}"

# Replace with your email and API token
email = "lukas.preidt@startstuttgart.org"

# Headers for the request
headers = {
    "Accept": "application/json"
}

# Making the GET request
response = requests.get(api_endpoint, headers=headers, auth=HTTPBasicAuth(email, api_token))

# Handling the response
if response.status_code == 200:
    ticket_data = response.json()
    print(f"Summary: {ticket_data['fields']['summary']}")
    print(f"Description: {ticket_data['fields']['description']}")
    print(f"Status: {ticket_data['fields']['status']['name']}")
else:
    print(f"Failed to fetch the ticket. HTTP Status Code: {response.status_code}")
    print(f"Response: {response.text}")
