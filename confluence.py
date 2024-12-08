import requests
import csv
import pandas as pd
from requests.auth import HTTPBasicAuth

# Confluence API Details
confluence_url = "https://one-atlas-nicz.atlassian.net/wiki/rest/api/content"
confluence_api_token = "ATATT3xFfGF0twe2_EsPpehBxwIxkodTEj2N-4iUr-7XMUVYPbUkeLgOqOJHBEjCgC_Z8GMir9NiA3oiBAV_D6IVleJ-7Mn5YZl6CXLdJOD6R8C59Ho6TyzvM314QZuE_GC2m1MIJEursbnLRZxJFRxhayF2Sbh-jb5jzoASDX-p8xTVUmlIwWA=39F389D8"
confluence_email = "marc.baumholz@startstuttgart.org"
space_key = "EO"  # Replace with your Confluence space key
parent_page_id = 3571986  # Replace with the parent page ID (if needed)

# Load AI summary from CSV using pandas
csv_file_path = "ai_summary.csv"  # Replace with the path to your CSV file
df = pd.read_csv(csv_file_path)
ai_summary = df['summary_text'].iloc[0]  # Assuming the summary is in the 'txt' column of the first row

# Prepare the Confluence page payload
confluence_payload = {
    "type": "page",
    "title": "AI-Generated Summary Page",
    "space": {
        "key": "EO"
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
