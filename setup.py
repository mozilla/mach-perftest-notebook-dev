import os
from setuptools import setup

"""
Sets up the CLI and modules for `mach-perftest-notebook`.
"""

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join(this_directory, "requirements.txt")) as f:
    install_requires = f.read()

setup(
    name="mach-perftest-notebook",
    version="0.0.1",
    author="Gregory Mierzwinski",
    author_email="gmierz1@live.ca",
    description=(
        "This tool will be used to standardize analysis/visualization techniques across Mozilla."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License Version 2.0 (MPLv2)",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/mozilla/mach-perftest-notebook-dev",
    packages=["perftestnotebook", "perftestnotebook.customtransforms"],
    install_requires=install_requires,
    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    perftestnotebook = perftestnotebook.perftestnotebook:main
    """,
)
