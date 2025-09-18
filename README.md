# hive-ai-JiraTestGen

Release Notes – AI Bot for Test Case Generation (v0.1.0)
Overview
This release introduces the AI-powered Test Case Generation Bot, a Python-based automation assistant that integrates Jira with local LLMs (via Ollama) to automatically generate, manage, and track test cases and test code from user stories.
✨ New Features
Jira Integration
Secure authentication with Jira Cloud using API tokens.
Automatically fetches user stories (summary + description).
Posts AI-generated test cases and code directly as Jira comments for full traceability.
LLM-Powered Test Case Generation
Connects to local LLMs (Ollama with Llama 3.1 or CodeLlama) for cost-effective and private code generation.
Generates:
Plain-English test cases.
Java RestAssured + JUnit API test classes.
(Planned) Python Playwright UI test cases.
Test Code Management
Generates structured code artifacts.
(Planned) Automatic commit of generated test code into GitHub/GitLab repositories with repo references linked back in Jira.
Feedback & Traceability
Adds AI-generated test cases and code back to Jira issues.
Establishes traceability between Jira stories, generated tests, and future CI/CD executions.
Execution Pipeline (Planned)
Integrate with CI/CD systems (GitHub Actions, Jenkins, GitLab CI).
Automatically run generated tests post-commit.
Push execution results (pass/fail) back into Jira.
🏗️ High-Level Architecture
Jira Integration Layer – Python (jira library / REST API)
LLM Integration Layer – Ollama (local) or OpenAI/Anthropic (cloud optional)
Test Code Generation – Java (API tests), Python (UI tests)
Repo Integration (Planned) – GitHub/GitLab API
CI/CD Feedback (Planned) – Jenkins, GitHub Actions, GitLab CI
🔄 Workflow
User creates a story in Jira.
Python agent fetches the story.
LLM generates test cases + code.
Output is stored in repos and linked back to Jira.
(Future) CI/CD runs generated tests and reports back to Jira.
🛠️ Tech Stack
Driver: Python
Jira Integration: jira Python library, Jira REST API
LLM: Ollama (Llama 3.1, CodeLlama, DeepSeek-Coder)
API Tests: Java (JUnit + RestAssured)
UI Tests: Python (Playwright)
Repo Integration: GitHub/GitLab API (planned)
CI/CD Feedback: GitHub Actions / Jenkins / GitLab CI (planned)
🐞 Known Issues
Ollama server may require manual restart if port 11434 is locked.
API test code generation only; UI test generation is not yet implemented.
Repository commit automation is not yet enabled.
📌 Next Steps
Add UI test case generation (Python + Playwright).
Implement repo integration (auto-commit tests to GitHub).
Enable CI/CD pipeline feedback loop to push test results into Jira.
Support multiple LLM backends (OpenAI, Anthropic, local models).
⚡ This release sets the foundation for end-to-end intelligent test automation: user stories → AI-generated tests → repository commits → CI/CD execution → Jira traceability.
