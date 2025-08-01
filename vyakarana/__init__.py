"""
Vyakarana: A Python package for Sanskrit Grammar data and analysis.

This package provides tools for working with Sanskrit grammatical data,
including sutras, dhatus (verbal roots), and other linguistic resources.
"""

from .models import (
    Sutra,
    SutraCollection,
    SutraIdentifier,
    SutraText,
    SutraReferences,
    SutraReference,
    SutraType,
    SutraTypeClassification,
    SutraTypeInfo,
    Vibhakti,
    Vachana,
    PadaAnalysis,
    PadaVibhaga,
    SutraCarryover,
    CarryoverType,
    Backlinks,
)
from .readers import read_sutras

__version__ = "0.1.0"
__author__ = "Arindam Saha"

__all__ = [
    "Sutra",
    "SutraCollection",
    "SutraIdentifier",
    "SutraText",
    "SutraReferences",
    "SutraReference",
    "SutraType",
    "SutraTypeClassification",
    "SutraTypeInfo",
    "Vibhakti",
    "Vachana",
    "PadaAnalysis",
    "PadaVibhaga",
    "SutraCarryover",
    "CarryoverType",
    "Backlinks",
    "read_sutras",
]
