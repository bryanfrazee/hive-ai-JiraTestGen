# tests/test_jiratestgen_full.py
import pytest
from unittest.mock import patch, MagicMock
from jiratestgen.jiratestgen import main

def test_main_pipeline(monkeypatch):
    monkeypatch.setenv("JIRA_API_TOKEN", "fake-token")
    fake_issue = MagicMock()
    fake_issue.fields.summary = "User logs in"
    fake_issue.fields.description = "As a user, I want to login."

    with patch("jiratestgen.jiratestgen.JIRA") as mock_jira_class:
        mock_jira_instance = mock_jira_class.return_value
        mock_jira_instance.issue.return_value = fake_issue
        mock_jira_instance.add_comment.return_value = None

        fake_response = {"response": "Generated test cases"}
        with patch("jiratestgen.jiratestgen.requests.post") as mock_post:
            mock_post.return_value.json.return_value = fake_response

            main("SCRUM-1")

            mock_jira_instance.issue.assert_called_once_with("SCRUM-1")
            mock_post.assert_called_once()
            mock_jira_instance.add_comment.assert_called_once_with(
                fake_issue,
                "AI-generated test cases and code:\n\nGenerated test cases"
            )
