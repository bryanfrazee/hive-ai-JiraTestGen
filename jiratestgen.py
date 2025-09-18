import os
import sys
import argparse
from jira import JIRA
import requests
import json

# --- 1. Command-line Arguments ---
parser = argparse.ArgumentParser(description="Generate AI test cases from Jira user story")
parser.add_argument("issue_key", help="The Jira issue key, e.g. SCRUM-1")
args = parser.parse_args()

# --- 2. Jira Setup ---
JIRA_SERVER = "https://hive-jiratestgen.atlassian.net"
JIRA_EMAIL = "bryanfrazee001@gmail.com"
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")  # store securely
ISSUE_KEY = args.issue_key   # <-- use parameter from command line

jira = JIRA(
    server=JIRA_SERVER,
    basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
)

# Get the Jira issue
issue = jira.issue(ISSUE_KEY)
user_story = issue.fields.summary + "\n" + (issue.fields.description or "")

print(f"📖 User Story from Jira ({ISSUE_KEY}):\n{user_story}\n")

# --- 3. Call Local LLM (Ollama) ---
prompt = f"""
You are a test automation assistant.
Read the following user story and generate:
1. 2-3 English test cases
2. A Java RestAssured JUnit test class for API testing.

User Story:
{user_story}
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
)

generated_output = response.json()["response"]
print("Generated Test Cases and Code:\n")
print(generated_output)

# --- 4. Add back to Jira ---
jira.add_comment(issue, f"AI-generated test cases and code:\n\n{generated_output}")
print(f"✅ Added AI-generated test cases back to Jira issue {ISSUE_KEY}!")
