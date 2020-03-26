import os
from setuptools import setup

"""
Sets up the CLI and modules for `mach-perftest-notebook`.
"""

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mach-perftest-notebook",
    version="0.0.1",
    author="Gregory Mierzwinski",
    author_email="gmierz1@live.ca",
    description=(
        "Development Repository for Mach Perftest Notebook Tooling. This tool will be used to standardize analysis/visualization techniques across Mozilla."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mozilla/mach-perftest-notebook-dev",
    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    perftestnotebook = perftestnotebook.perftestnotebook:main
    """,
)
