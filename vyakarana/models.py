"""
Data models for Sanskrit Grammar (Vyakarana) entities.

This module defines dataclasses for representing Sanskrit grammatical concepts
like sutras, with proper type annotations and validation.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Sutra:
    """
    Represents a Sanskrit grammar sutra with all its associated metadata.

    Attributes:
        i: Unique identifier for the sutra
        a: Adhyaya (chapter) number
        p: Pada (quarter) number
        n: Sutra number within the pada
        s: Sanskrit text of the sutra
        e: English transliteration
        skn: Siddhanta Kaumudi number
        lskn: Laghu Siddhanta Kaumudi number
        mskn: Madhya Siddhanta Kaumudi number
        sskn: Sara Siddhanta Kaumudi number
        plskn: Paribhasha Laghu Siddhanta Kaumudi number
        lpn: Laghu Prakriya number
        pc: Parsed components
        sk_chapter: Siddhanta Kaumudi chapter
        lsk_chapter: Laghu Siddhanta Kaumudi chapter
        type: Type classification of the sutra
        an: Anuvrutti (continuation from previous sutras)
        ad: Additional data
        ss: Sanskrit with sandhi
        rpn: Reference/position number
    """

    i: str
    a: str
    p: str
    n: str
    s: str  # Sanskrit text
    e: str  # English transliteration
    skn: str
    lskn: str
    mskn: str
    sskn: str
    plskn: str
    lpn: str
    pc: str  # Parsed components
    sk_chapter: str
    lsk_chapter: str
    type: str
    an: str  # Anuvrutti
    ad: str  # Additional data
    ss: str  # Sanskrit with sandhi
    rpn: str

    @property
    def adhyaya(self) -> int:
        """Return the adhyaya (chapter) as an integer."""
        return int(self.a)

    @property
    def pada(self) -> int:
        """Return the pada (quarter) as an integer."""
        return int(self.p)

    @property
    def number(self) -> int:
        """Return the sutra number within the pada as an integer."""
        return int(self.n)

    @property
    def reference(self) -> str:
        """Return a formatted reference like '1.1.1'."""
        return f"{self.a}.{self.p}.{self.n}"

    @property
    def devanagari(self) -> str:
        """Return the Sanskrit text in Devanagari."""
        return self.s

    @property
    def transliteration(self) -> str:
        """Return the English transliteration."""
        return self.e

    def __str__(self) -> str:
        """Return a readable string representation."""
        return f"Sutra {self.reference}: {self.s}"

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"Sutra(reference='{self.reference}', text='{self.s}')"


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
            search_fields = [sutra.s, sutra.e, sutra.ss]
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
