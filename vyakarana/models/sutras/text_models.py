"""
Text and reference models for Sanskrit Grammar (Vyakarana) entities.

This module defines classes for handling text content and reference information.
"""

from dataclasses import dataclass


@dataclass
class SutraText:
    """
    Represents the text content of a sutra in different scripts/languages.

    Attributes:
        sanskrit: Sanskrit text in Devanagari script
        english: English transliteration
    """

    sanskrit: str  # Sanskrit text in Devanagari
    english: str  # English transliteration

    @property
    def devanagari(self) -> str:
        """Return the Sanskrit text in Devanagari (alias for sanskrit)."""
        return self.sanskrit

    @property
    def transliteration(self) -> str:
        """Return the English transliteration (alias for english)."""
        return self.english

    def __str__(self) -> str:
        """Return a readable string representation."""
        return self.sanskrit

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"SutraText(sanskrit='{self.sanskrit}', english='{self.english}')"


@dataclass
class SutraReferences:
    """
    Represents various reference numbers and chapter information for a sutra.

    Attributes:
        skn: Siddhanta Kaumudi number
        lskn: Laghu Siddhanta Kaumudi number
        mskn: Madhya Siddhanta Kaumudi number
        sskn: Sara Siddhanta Kaumudi number
        plskn: Paribhasha Laghu Siddhanta Kaumudi number
        lpn: Laghu Prakriya number
        sk_chapter: Siddhanta Kaumudi chapter
        lsk_chapter: Laghu Siddhanta Kaumudi chapter
    """

    skn: int  # Siddhanta Kaumudi number
    lskn: int  # Laghu Siddhanta Kaumudi number
    mskn: int  # Madhya Siddhanta Kaumudi number
    sskn: int  # Sara Siddhanta Kaumudi number
    plskn: int  # Paribhasha Laghu Siddhanta Kaumudi number
    lpn: int  # Laghu Prakriya number
    sk_chapter: int  # Siddhanta Kaumudi chapter
    lsk_chapter: int  # Laghu Siddhanta Kaumudi chapter

    def __str__(self) -> str:
        """Return a readable string representation."""
        return f"SutraReferences(skn={self.skn}, lskn={self.lskn})"

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return (
            f"SutraReferences(skn={self.skn}, lskn={self.lskn}, mskn={self.mskn}, "
            f"sskn={self.sskn}, plskn={self.plskn}, lpn={self.lpn}, "
            f"sk_chapter={self.sk_chapter}, lsk_chapter={self.lsk_chapter})"
        )
