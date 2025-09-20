# setup.py
from setuptools import setup, find_packages

setup(
    name="jiratestgen",
    version="0.1.0",
    packages=find_packages("src"),        # find packages inside src/
    package_dir={"": "src"},              # map package root to src/
    install_requires=[
        "requests",
        "jira",
    ],
    entry_points={
        "console_scripts": [
            # optional CLI entry point
            # user can run: jiratestgen SCRUM-1
            "jiratestgen=jiratestgen.jiratestgen:main",
        ],
    },
)
