#!/usr/bin/env python3
"""
Setup script for the Vyakarana Sanskrit Grammar package.
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vyakarana",
    version="0.1.0",
    author="Arindam Saha",
    author_email="arindamsaha1507@gmail.com",
    description="A Python package for Sanskrit Grammar (Vyakarana) data and analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arindamsaha1507/vyakarana",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
            "bandit>=1.7.0",
            "coverage>=7.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "coverage>=7.0.0",
        ],
        "security": [
            "bandit>=1.7.0",
            "safety>=2.3.0",
            "pip-audit>=2.6.0",
        ],
    },
    package_data={
        "vyakarana": [
            "data/*.txt",
            "data/*.json",
        ],
    },
    include_package_data=True,
)
