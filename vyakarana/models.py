"""
Data models for Sanskrit Grammar (Vyakarana) entities.

This module defines dataclasses for representing Sanskrit grammatical concepts
like sutras, with proper type annotations and validation.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SutraIdentifier:
    """
    Represents a unique identifier for a Sanskrit grammar sutra.

    Attributes:
        adhyaya: Adhyaya (chapter) number (1-8)
        pada: Pada (quarter) number (1-4)
        number: Sutra number within the pada
    """

    adhyaya: int  # Adhyaya (chapter) - range 1-8
    pada: int  # Pada (quarter) - range 1-4
    number: int  # Sutra number within the pada

    def __post_init__(self):
        """Validate the sutra identifiers after initialization."""
        if not (1 <= self.adhyaya <= 8):
            raise ValueError(f"Adhyaya must be between 1 and 8, got {self.adhyaya}")
        if not (1 <= self.pada <= 4):
            raise ValueError(f"Pada must be between 1 and 4, got {self.pada}")
        if self.number < 1:
            raise ValueError(f"Sutra number must be positive, got {self.number}")

    @property
    def reference(self) -> str:
        """Return a formatted reference like '1.1.1'."""
        return f"{self.adhyaya}.{self.pada}.{self.number}"

    def __str__(self) -> str:
        """Return a readable string representation."""
        return self.reference

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"SutraIdentifier(adhyaya={self.adhyaya}, pada={self.pada}, number={self.number})"


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


@dataclass
class Sutra:
    """
    Represents a Sanskrit grammar sutra with all its associated metadata.

    Attributes:
        identifier: Unique identifier for the sutra (SutraIdentifier object)
        text: Text content of the sutra (SutraText object)
        references: Reference numbers and chapters (SutraReferences object)
        pc: Parsed components
        type: Type classification of the sutra
        an: Anuvrutti (continuation from previous sutras)
        ad: Additional data
        ss: Sanskrit with sandhi
    """

    identifier: SutraIdentifier
    text: SutraText
    references: SutraReferences
    pc: str  # Parsed components
    type: str
    an: str  # Anuvrutti
    ad: str  # Additional data
    ss: str  # Sanskrit with sandhi

    @property
    def adhyaya(self) -> int:
        """Return the adhyaya (chapter) as an integer."""
        return self.identifier.adhyaya

    @property
    def pada(self) -> int:
        """Return the pada (quarter) as an integer."""
        return self.identifier.pada

    @property
    def number(self) -> int:
        """Return the sutra number within the pada as an integer."""
        return self.identifier.number

    @property
    def reference(self) -> str:
        """Return a formatted reference like '1.1.1'."""
        return self.identifier.reference

    @property
    def skn(self) -> int:
        """Return the Siddhanta Kaumudi number."""
        return self.references.skn

    @property
    def lskn(self) -> int:
        """Return the Laghu Siddhanta Kaumudi number."""
        return self.references.lskn

    @property
    def sk_chapter(self) -> int:
        """Return the Siddhanta Kaumudi chapter."""
        return self.references.sk_chapter

    @property
    def lsk_chapter(self) -> int:
        """Return the Laghu Siddhanta Kaumudi chapter."""
        return self.references.lsk_chapter

    @property
    def devanagari(self) -> str:
        """Return the Sanskrit text in Devanagari."""
        return self.text.devanagari

    @property
    def transliteration(self) -> str:
        """Return the English transliteration."""
        return self.text.transliteration

    def __str__(self) -> str:
        """Return a readable string representation."""
        return f"Sutra {self.reference}: {self.text.sanskrit}"

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"Sutra(reference='{self.reference}', text='{self.text.sanskrit}')"


@dataclass
class SutraCollection:
    """
    Represents a collection of sutras with metadata.

    Attributes:
        name: Name of the collection
        sutras: List of Sutra objects
    """

    name: str
    sutras: List[Sutra]

    def __len__(self) -> int:
        """Return the number of sutras in the collection."""
        return len(self.sutras)

    def __iter__(self):
        """Allow iteration over sutras."""
        return iter(self.sutras)

    def __getitem__(self, index) -> Sutra:
        """Allow indexing into the sutra collection."""
        return self.sutras[index]

    def get_by_reference(self, reference: str) -> Optional[Sutra]:
        """
        Get a sutra by its reference (e.g., '1.1.1').

        Args:
            reference: The sutra reference in format 'a.p.n'

        Returns:
            The Sutra object if found, None otherwise
        """
        for sutra in self.sutras:
            if sutra.reference == reference:
                return sutra
        return None

    def get_by_adhyaya(self, adhyaya: int) -> List[Sutra]:
        """
        Get all sutras from a specific adhyaya (chapter).

        Args:
            adhyaya: The chapter number

        Returns:
            List of Sutra objects from that chapter
        """
        return [sutra for sutra in self.sutras if sutra.adhyaya == adhyaya]

    def get_by_pada(self, adhyaya: int, pada: int) -> List[Sutra]:
        """
        Get all sutras from a specific pada within an adhyaya.

        Args:
            adhyaya: The chapter number
            pada: The quarter number

        Returns:
            List of Sutra objects from that pada
        """
        return [
            sutra
            for sutra in self.sutras
            if sutra.adhyaya == adhyaya and sutra.pada == pada
        ]

    def search_text(self, text: str, case_sensitive: bool = False) -> List[Sutra]:
        """
        Search for sutras containing specific text.

        Args:
            text: Text to search for
            case_sensitive: Whether the search should be case sensitive

        Returns:
            List of Sutra objects containing the text
        """
        if not case_sensitive:
            text = text.lower()

        results = []
        for sutra in self.sutras:
            search_fields = [sutra.text.sanskrit, sutra.text.english, sutra.ss]
            for field in search_fields:
                field_text = field if case_sensitive else field.lower()
                if text in field_text:
                    results.append(sutra)
                    break

        return results

    def __str__(self) -> str:
        """Return a readable string representation."""
        return f"SutraCollection(name='{self.name}', count={len(self.sutras)})"

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"SutraCollection(name='{self.name}', sutras={len(self.sutras)} items)"
