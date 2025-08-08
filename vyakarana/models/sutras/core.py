"""
Core models for Sanskrit Grammar (Vyakarana) entities.

This module defines the main Sutra and SutraCollection classes.
"""

from dataclasses import dataclass
from typing import List, Optional

from .analysis import PadaVibhaga
from .carryover import Backlinks, SutraCarryover
from .classification import SutraTypeClassification, SutraTypeInfo
from .enums import SutraType
from .identifiers import SutraIdentifier, SutraReference
from .text_models import SutraReferences, SutraText


@dataclass
class Sutra:
    """
    Represents a Sanskrit grammar sutra with all its associated metadata.

    Attributes:
        identifier: Unique identifier for the sutra (SutraIdentifier object)
        text: Text content of the sutra (SutraText object)
        references: Reference numbers and chapters (SutraReferences object)
        pada_vibhaga: Grammatical analysis of the sutra words (PadaVibhaga object)
        sutra_type_info: Type classifications of the sutra (SutraTypeInfo object)
        backlinks: Backlinks to previous sutras (anuvritti and adhikara)
        ss: Sanskrit with sandhi
    """

    identifier: SutraIdentifier
    text: SutraText
    references: SutraReferences
    pada_vibhaga: Optional[PadaVibhaga]  # Grammatical analysis
    sutra_type_info: SutraTypeInfo  # Type classifications of the sutra
    backlinks: Backlinks  # Backlinks to previous sutras (anuvritti and adhikara)
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

    @property
    def sanskrit(self) -> str:
        """Return the Sanskrit text."""
        return self.text.sanskrit

    @property
    def english(self) -> str:
        """Return the English text."""
        return self.text.english

    @property
    def sutra_types(self) -> List[SutraType]:
        """Return a list of all sutra types."""
        return self.sutra_type_info.types

    @property
    def type_classifications(self) -> List[SutraTypeClassification]:
        """Return all type classifications with explanations."""
        return self.sutra_type_info.classifications

    @property
    def anuvritti(self) -> SutraCarryover:
        """Return the anuvritti carryover (for backward compatibility)."""
        return self.backlinks.anuvritti

    @property
    def adhikara(self) -> SutraCarryover:
        """Return the adhikara carryover (for backward compatibility)."""
        return self.backlinks.adhikara

    @property
    def has_anuvritti(self) -> bool:
        """Return True if there is anuvritti content."""
        return self.backlinks.has_anuvritti

    @property
    def has_adhikara(self) -> bool:
        """Return True if there is adhikara content."""
        return self.backlinks.has_adhikara

    @property
    def has_any_carryover(self) -> bool:
        """Return True if there is any carryover content."""
        return self.backlinks.has_any_carryover

    def has_type(self, sutra_type: SutraType) -> bool:
        """
        Check if this sutra has a specific type classification.

        Args:
            sutra_type: The SutraType to check for

        Returns:
            True if the sutra has this type classification, False otherwise
        """
        return sutra_type in self.sutra_types

    def __str__(self) -> str:
        """Return a readable string representation."""
        return f"Sutra {self.reference}: {self.text.sanskrit}"

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"Sutra(reference='{self.reference}', text='{self.text.sanskrit}')"

    def __eq__(self, other) -> bool:
        """Check equality based on sutra identifier."""
        if not isinstance(other, Sutra):
            return False
        return self.identifier == other.identifier

    def __lt__(self, other) -> bool:
        """Compare ordering based on sutra identifier (adhyaya, pada, number)."""
        if not isinstance(other, Sutra):
            return NotImplemented
        return self.identifier < other.identifier

    def __le__(self, other) -> bool:
        """Less than or equal comparison."""
        if not isinstance(other, Sutra):
            return NotImplemented
        return self.identifier <= other.identifier

    def __gt__(self, other) -> bool:
        """Greater than comparison."""
        if not isinstance(other, Sutra):
            return NotImplemented
        return self.identifier > other.identifier

    def __ge__(self, other) -> bool:
        """Greater than or equal comparison."""
        if not isinstance(other, Sutra):
            return NotImplemented
        return self.identifier >= other.identifier

    def __hash__(self) -> int:
        """Return hash value for use in sets and dictionaries."""
        return hash(self.identifier)


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

    def get_by_reference(self, reference: SutraReference | str) -> Optional[Sutra]:
        """
        Get a sutra by its reference (e.g., '1.1.1').

        Args:
            reference: The sutra reference in format 'a.p.n'

        Returns:
            The Sutra object if found, None otherwise
        """

        if isinstance(reference, SutraReference):
            reference = reference.reference_string

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

    def get_sorted(self) -> List[Sutra]:
        """
        Get all sutras in sorted order by (adhyaya, pada, number).

        Returns:
            List of Sutra objects sorted by their identifier
        """
        return sorted(self.sutras)

    def __str__(self) -> str:
        """Return a readable string representation."""
        return f"SutraCollection(name='{self.name}', count={len(self.sutras)})"

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"SutraCollection(name='{self.name}', sutras={len(self.sutras)} items)"
