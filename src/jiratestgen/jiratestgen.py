# src/jiratestgen/jiratestgen.py
import os
import requests
from jira import JIRA

JIRA_SERVER = "https://hive-jiratestgen.atlassian.net"
JIRA_EMAIL = "bryanfrazee001@gmail.com"

def get_jira_issue(issue_key: str, jira_token: str):
    jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, jira_token))
    issue = jira.issue(issue_key)
    user_story = issue.fields.summary + "\n" + (issue.fields.description or "")
    return issue, user_story

def generate_tests_from_llm(user_story: str):
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
        json={"model": "llama3", "prompt": prompt, "stream": False}
    )
    return response.json()["response"]

def add_comment_to_jira(issue, comment: str, jira_token: str):
    jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, jira_token))
    jira.add_comment(issue, comment)

def main(issue_key: str):
    jira_token = os.getenv("JIRA_API_TOKEN")
    if not jira_token:
        print("❌ Error: JIRA_API_TOKEN environment variable is missing!")
        return

    issue, user_story = get_jira_issue(issue_key, jira_token)
    print(f"📖 User Story:\n{user_story}\n")

    generated_output = generate_tests_from_llm(user_story)
    print("Generated Test Cases and Code:\n")
    print(generated_output)

    add_comment_to_jira(issue, f"AI-generated test cases and code:\n\n{generated_output}", jira_token)
    print(f"✅ Added AI-generated test cases back to Jira issue {issue_key}!")

# --- CLI entry point ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate AI test cases from Jira user story")
    parser.add_argument("issue_key", help="The Jira issue key, e.g. SCRUM-1")
    args = parser.parse_args()
    print(f"Running jiratestgen for issue: {args.issue_key}")
    main(args.issue_key)
