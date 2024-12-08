import requests
from requests.auth import HTTPBasicAuth
import yaml
import csv
import pandas as pd

# Load configurations (Jira and OpenAI tokens)
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
    jira_api_token = config["jira"]["api_token"]
    jira_email = config["jira"]["credentials"]["email"]
    openai_api_token = config["openai"]["api_token"]

# Jira Cloud URL and ticket details
jira_url = "https://one-atlas-nicz.atlassian.net/"

# TODO: ganzen inhalt der jira seite holen => in eine DB packen mit den APIs von Jira
ticket_key = "DESIGN-2"  # Replace with your ticket key
jira_api_endpoint = f"{jira_url}/rest/api/3/issue/{ticket_key}"

# Headers for Jira request
jira_headers = {"Accept": "application/json"}

# Fetch ticket details from Jira
response = requests.get(jira_api_endpoint, headers=jira_headers, auth=HTTPBasicAuth(jira_email, jira_api_token))

if response.status_code == 200:
    # Parse Jira ticket details
    ticket_data = response.json()
    summary = ticket_data['fields']['summary']
    description = ticket_data['fields']['description']
    status = ticket_data['fields']['status']['name']

    print(f"Summary: {summary}")
    print(f"Description: {description}")
    print(f"Status: {status}")
    #daten extrahiern => weiter schritte GPT prompting => summary => KPIs definiere => extrahierne => DOD => Main goal => kernaussagen in bulletpoitns => Persona schriebt sowas 

    # Send details to OpenAI for analysis
    openai_url = "https://api.openai.com/v1/chat/completions"
    openai_headers = {
        "Authorization": f"Bearer {openai_api_token}",
        "Content-Type": "application/json"
    }
    openai_payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes Jira tickets."},
            {"role": "user", "content": f"Here is the Jira ticket information:\nSummary: {summary}\nDescription: {description}\nStatus: {status}\n\nPlease provide a concise summary."}
        ],
        "temperature": 0.7
    }

    openai_response = requests.post(openai_url, json=openai_payload, headers=openai_headers)

    if openai_response.status_code == 200:
        ai_data = openai_response.json()
        ai_summary = ai_data['choices'][0]['message']['content']
        print("\nAI-Generated Summary:")
        print(ai_summary)
        
        # Save the AI summary into a pandas DataFrame
        df = pd.DataFrame([{"summary": "AI-Generated Summary", "summary_text": ai_summary}])
        
        # Save the DataFrame to a CSV file
        df.to_csv("ai_summary.csv", index=False)
        print("AI summary saved to 'ai_summary.csv'")
    else:
        print(f"Failed to analyze with OpenAI. HTTP Status Code: {openai_response.status_code}")
        print(openai_response.text)
else:
    print(f"Failed to fetch the ticket. HTTP Status Code: {response.status_code}")
    print(response.text)

