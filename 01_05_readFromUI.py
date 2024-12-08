import requests
import csv
import pandas as pd
from requests.auth import HTTPBasicAuth
import yaml
from bs4 import BeautifulSoup

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
    jira_api_token = config["jira"]["api_token"]
    confluence_email = config["jira"]["credentials"]["email"]

# Confluence API Details
confluence_url = "https://one-atlas-nicz.atlassian.net/wiki/rest/api/content"
page_id = "3637282"  # Replace with the page ID of your Confluence page

# Headers for the API request
headers = {
    "Authorization": f"Bearer {jira_api_token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Step 1: Get the Confluence page content
response = requests.get(f"{confluence_url}/{page_id}?expand=body.storage", headers=headers, auth=HTTPBasicAuth(confluence_email, jira_api_token))  # Basic Auth using email and token)

if response.status_code == 200:
    page_content = response.json()
    html_content = page_content["body"]["storage"]["value"]
    
    # Step 2: Parse the HTML to extract links
    soup = BeautifulSoup(html_content, "html.parser")
    links = [{"Category": link.get_text(strip=True), "URL": link.get("href")} for link in soup.find_all("a", href=True)]
    
    # Step 3: Save the links in a DataFrame
    df = pd.DataFrame(links)
    print("Extracted Links:")
    print(df)
    
    # Step 4: Export to CSV (optional)
    df.to_csv("./data/confluence_links.csv", index=False)
    print("Links saved to confluence_links.csv")
else:
    print(f"Failed to fetch the page content. Status Code: {response.status_code}")
    print(response.text)
