"""
Pytest configuration and shared fixtures for Vyakarana tests.
"""

from pathlib import Path

import pytest

from vyakarana import read_sutras

# pylint: disable=redefined-outer-name


@pytest.fixture(scope="session")
def data_file():
    """Session-scoped fixture to provide the data file path."""
    current_dir = Path(__file__).parent
    return current_dir.parent / "sutraani" / "data.txt"


@pytest.fixture(scope="session")
def sample_collection(data_file):
    """Session-scoped fixture to provide a loaded sutra collection."""
    return read_sutras(data_file)
