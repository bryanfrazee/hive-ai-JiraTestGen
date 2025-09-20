# tests/test_jiratestgen_mock.py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

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

def test_generate_tests_from_llm_mock():
    fake_response = {"response": "Generated test code"}
    with patch("jiratestgen.jiratestgen.requests.post") as mock_post:
        mock_post.return_value.json.return_value = fake_response
        output = generate_tests_from_llm("Some user story")
        assert output == "Generated test code"

def test_add_comment_to_jira_mock():
    fake_issue = MagicMock()
    with patch("jiratestgen.jiratestgen.JIRA") as mock_jira:
        mock_instance = mock_jira.return_value
        add_comment_to_jira(fake_issue, "Comment", "fake-token")
        mock_instance.add_comment.assert_called_once_with(fake_issue, "Comment")
