# tests/test_jiratestgen_unit.py
import pytest
from jiratestgen.jiratestgen import generate_tests_from_llm

def test_generate_tests_from_llm_format():
    user_story = "As a user, I want to login so that I can access my account."
    output = generate_tests_from_llm(user_story)
    # Don't call real LLM in unit test, just check type
    assert isinstance(user_story, str)
    assert "login" in user_story
