"""
Readers package for Sanskrit Grammar (Vyakarana) data files.

This package contains modules for reading different types of Sanskrit
grammatical data files.
"""

# Import the main reader function for backward compatibility
from .ashtadhyayi_readers import read_sutras

__all__ = [
    "read_sutras",
]
