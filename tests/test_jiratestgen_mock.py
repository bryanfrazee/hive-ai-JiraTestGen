# tests/test_jiratestgen_mock.py
import pytest
from unittest.mock import patch, MagicMock
from jiratestgen.jiratestgen import get_jira_issue, generate_tests_from_llm, add_comment_to_jira

def test_get_jira_issue_mock():
    fake_issue = MagicMock()
    fake_issue.fields.summary = "Test summary"
    fake_issue.fields.description = "Test description"

    with patch("jiratestgen.jiratestgen.JIRA") as mock_jira:
        mock_jira.return_value.issue.return_value = fake_issue
        issue, user_story = get_jira_issue("SCRUM-1", "fake-token")
        assert issue.fields.summary == "Test summary"
        assert "Test description" in user_story
