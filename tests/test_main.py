# test_main.py
import pytest
from unittest.mock import patch, MagicMock
import generate_tests

@pytest.fixture
def fake_jira_issue():
    issue = MagicMock()
    issue.fields.summary = "As a user, I want to login"
    issue.fields.description = "So I can access my account"
    return issue

@pytest.fixture
def fake_llm_response():
    return {"response": "Test1: ...\nTest2: ...\npublic class ApiTest {...}"}

def test_main_workflow(monkeypatch, fake_jira_issue, fake_llm_response):
    # Patch command-line args
    monkeypatch.setattr("sys.argv", ["generate_tests.py", "SCRUM-123"])
    # Patch environment variable
    monkeypatch.setenv("JIRA_API_TOKEN", "fake_token")

    # Mock Jira class
    mock_jira_instance = MagicMock()
    mock_jira_instance.issue.return_value = fake_jira_issue
    mock_jira_instance.add_comment = MagicMock()

    # Patch JIRA and requests.post
    with patch("generate_tests.JIRA", return_value=mock_jira_instance) as mock_jira_class:
        with patch("generate_tests.requests.post") as mock_post:
            mock_post.return_value.json.return_value = fake_llm_response

            # Run main()
            generate_tests.main()

    # --- Assertions ---
    # Jira instance called with correct credentials
    mock_jira_class.assert_called_once_with(
        server="<your-jira-server-url>",
        basic_auth=("<your-jira-linked-email>", "fake_token")
    )
    # Jira issue retrieved
    mock_jira_instance.issue.assert_called_once_with("SCRUM-123")
    # LLM API called
    payload = mock_post.call_args[1]["json"]
    assert "As a user, I want to login" in payload["prompt"]
    assert payload["model"] == "llama3"
    # Comment added back to Jira
    mock_jira_instance.add_comment.assert_called_once()
    args, kwargs = mock_jira_instance.add_comment.call_args
    assert "AI-generated test cases and code" in args[1]
    assert "Test1: ..." in args[1]
