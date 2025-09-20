# test_generate_tests.py
import os
import pytest
from unittest.mock import patch, MagicMock
import generate_tests

# --- Fixtures ---
@pytest.fixture
def fake_jira_issue():
    issue = MagicMock()
    issue.fields.summary = "As a user, I want to login"
    issue.fields.description = "So I can access my account"
    return issue

@pytest.fixture
def fake_llm_response():
    return {"response": "Test1: ...\nTest2: ...\npublic class ApiTest {...}"}

# --- Test parse_args ---
def test_parse_args(monkeypatch):
    monkeypatch.setattr("sys.argv", ["generate_tests.py", "SCRUM-123"])
    args = generate_tests.parse_args()
    assert args.issue_key == "SCRUM-123"

# --- Test get_jira_issue ---
@patch("generate_tests.JIRA")
def test_get_jira_issue(mock_jira, fake_jira_issue):
    mock_jira.return_value.issue.return_value = fake_jira_issue
    jira, issue = generate_tests.get_jira_issue("SCRUM-123", "server", "email", "token")
    mock_jira.assert_called_once_with(server="server", basic_auth=("email", "token"))
    assert issue.fields.summary == "As a user, I want to login"

# --- Test generate_llm_tests ---
@patch("generate_tests.requests.post")
def test_generate_llm_tests(mock_post, fake_llm_response):
    mock_post.return_value.json.return_value = fake_llm_response
    output = generate_tests.generate_llm_tests("user story text")
    assert "Test1: ..." in output
    mock_post.assert_called_once()
    payload = mock_post.call_args[1]["json"]
    assert "user story text" in payload["prompt"]
    assert payload["model"] == "llama3"

# --- Test add_jira_comment ---
def test_add_jira_comment(fake_jira_issue):
    mock_jira = MagicMock()
    generate_tests.add_jira_comment(mock_jira, fake_jira_issue, "content")
    mock_jira.add_comment.assert_called_once_with(fake_jira_issue, "content")
