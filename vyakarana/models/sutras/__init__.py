"""
Sutra Models Package

This package contains all data models related to Sanskrit grammar sutras,
including identifiers, text models, analysis, classification, carryover
mechanisms, and core sutra representations.
"""

from .analysis import PadaAnalysis, PadaVibhaga

# Import carryover classes (depend on enums and identifiers)
from .carryover import Backlinks, SutraCarryover
from .classification import SutraTypeClassification, SutraTypeInfo

# Import core classes (depend on all others)
from .core import Sutra, SutraCollection

# Import enums first (no dependencies)
from .enums import CarryoverType, SutraType, Vachana, Vibhakti

# Import base classes (depend on enums)
from .identifiers import SutraIdentifier, SutraReference
from .text_models import SutraReferences, SutraText

# Public API
__all__ = [
    # Enums
    "Vibhakti",
    "Vachana",
    "SutraType",
    "CarryoverType",
    # Identifiers
    "SutraIdentifier",
    "SutraReference",
    # Text models
    "SutraText",
    "SutraReferences",
    # Analysis
    "PadaAnalysis",
    "PadaVibhaga",
    # Classification
    "SutraTypeClassification",
    "SutraTypeInfo",
    # Carryover
    "SutraCarryover",
    "Backlinks",
    # Core
    "Sutra",
    "SutraCollection",
]
