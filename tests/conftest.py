"""
Pytest configuration and shared fixtures for Vyakarana tests.
"""

import sys
from pathlib import Path

import pytest

# Add the parent directory to the path to import vyakarana
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def data_file():
    """Session-scoped fixture to provide the data file path."""
    current_dir = Path(__file__).parent
    return current_dir.parent / "sutraani" / "data.txt"


@pytest.fixture(scope="session")
def sample_collection(data_file):
    """Session-scoped fixture to provide a loaded sutra collection."""
    from vyakarana import read_sutras
    return read_sutras(data_file)
