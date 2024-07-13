from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="avcheck",
    version="0.1.2",
    description="Python library to interact with AvCheck API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="NullBulge",
    author_email="contact@nullbulge.se",
    url="https://github.com/NullBulgeOfficial/AVCheck-Python",
    project_urls={
        "Bug Tracker": "https://github.com/NullBulgeOfficial/AVCheck-Python/issues",
        "Source Code": "https://github.com/NullBulgeOfficial/AVCheck-Python",
    },
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)