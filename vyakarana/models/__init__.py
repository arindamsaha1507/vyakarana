"""
Models package for Sanskrit Grammar (Vyakarana) entities.

This package contains all the data models used in the vyakarana library,
organized by grammatical entity type (sutras, dhatus, vartikas, etc.).
"""

# Import all sutra-related models from the sutras subpackage
from .sutras import (
    # Enums
    Vibhakti,
    Vachana,
    SutraType,
    CarryoverType,
    # Identifiers
    SutraIdentifier,
    SutraReference,
    # Text models
    SutraText,
    SutraReferences,
    # Analysis
    PadaAnalysis,
    PadaVibhaga,
    # Classification
    SutraTypeClassification,
    SutraTypeInfo,
    # Carryover
    SutraCarryover,
    Backlinks,
    # Core
    Sutra,
    SutraCollection,
)

# Public API - maintain backward compatibility
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
