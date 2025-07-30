"""
Enums for Sanskrit Grammar (Vyakarana) entities.

This module defines enums used throughout the vyakarana package.
"""

from enum import Enum


class Vibhakti(Enum):
    """Sanskrit case endings (vibhakti)."""

    PRATHAMA = 1  # Nominative
    DVITIYA = 2  # Accusative
    TRITIYA = 3  # Instrumental
    CHATURTHI = 4  # Dative
    PANCHAMI = 5  # Ablative
    SHASHTHI = 6  # Genitive
    SAPTAMI = 7  # Locative
    SAMBODHANA = 8  # Vocative
    AVYAYA = 0  # Indeclinable (special case)


class Vachana(Enum):
    """Sanskrit number (vachana)."""

    EKAVACHANA = 1  # Singular
    DVIVACHANA = 2  # Dual
    BAHUVACHANA = 3  # Plural
    AVYAYA = 0  # Indeclinable (special case)


class SutraType(Enum):
    """Types of Sanskrit grammar sutras (only those present in the data)."""

    SANJNA = "S"  # Definition
    PARIBHASHA = "P"  # Technical rule
    VIDHI = "V"  # Injunction
    ATIDESHA = "AT"  # Extension
    ADHIKARA = "AD"  # Governing rule


class CarryoverType(Enum):
    """Types of sutra carryover references."""

    ANUVRITTI = "anuvritti"  # Continuation/carryover of words/meanings
    ADHIKARA = "adhikara"  # Governing rules that apply over ranges
