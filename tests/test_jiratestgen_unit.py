# tests/test_jiratestgen_unit.py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from jiratestgen.jiratestgen import generate_tests_from_llm

def test_generate_tests_from_llm_format():
    user_story = "As a user, I want to login so that I can access my account."
    assert isinstance(user_story, str)
    assert "login" in user_story
