"""
Data models for Sanskrit Grammar (Vyakarana) entities.

This module defines dataclasses for representing Sanskrit grammatical concepts
like sutras, with proper type annotations and validation.
"""

from dataclasses import dataclass
from typing import List, Optional
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


@dataclass
class SutraTypeClassification:
    """
    Represents a single type classification of a sutra with optional explanation.

    Attributes:
        sutra_type: The type of the sutra (SutraType enum)
        explanation: Optional Sanskrit explanation for this classification
    """

    sutra_type: SutraType
    explanation: Optional[str] = None

    def __str__(self) -> str:
        """Return a readable string representation."""
        if self.explanation:
            return f"{self.sutra_type.name} ({self.explanation})"
        return self.sutra_type.name

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"SutraTypeClassification(sutra_type={self.sutra_type}, explanation='{self.explanation}')"


@dataclass
class SutraTypeInfo:
    """
    Represents the complete type information for a sutra.
    A sutra can have multiple type classifications.

    Attributes:
        classifications: List of SutraTypeClassification objects
    """

    classifications: List[SutraTypeClassification]

    def __len__(self) -> int:
        """Return the number of classifications."""
        return len(self.classifications)

    def __iter__(self):
        """Allow iteration over classifications."""
        return iter(self.classifications)

    def __getitem__(self, index) -> SutraTypeClassification:
        """Allow indexing into the classifications."""
        return self.classifications[index]

    @property
    def types(self) -> List[SutraType]:
        """Return a list of all sutra types."""
        return [c.sutra_type for c in self.classifications]

    @classmethod
    def from_string(cls, type_string: str) -> "SutraTypeInfo":
        """
        Parse a type string into SutraTypeInfo.

        Format: TYPE$explanation$##TYPE$explanation$##...
        Example: "P$व्यपदेशिवद्भावज्ञापकपरिभाषा$##AT$आद्यन्तवदतिदेशः$"

        Args:
            type_string: The type string from the data

        Returns:
            SutraTypeInfo object with parsed classifications
        """
        if not type_string or type_string.strip() == "":
            return cls([])

        classifications = []
        # Split by ## to get individual classifications
        parts = type_string.split("##")

        for part in parts:
            if not part.strip():
                continue

            # Split by $ to get type and explanation
            components = part.split("$")
            if len(components) >= 1 and components[0]:
                type_id = components[0].strip()
                explanation = (
                    components[1].strip()
                    if len(components) > 1 and components[1].strip()
                    else None
                )

                # Convert type_id to SutraType enum
                try:
                    sutra_type = SutraType(type_id)
                    classification = SutraTypeClassification(
                        sutra_type=sutra_type, explanation=explanation
                    )
                    classifications.append(classification)
                except ValueError:
                    # Skip unknown type identifiers
                    continue

        return cls(classifications)

    def __str__(self) -> str:
        """Return a readable string representation."""
        if not self.classifications:
            return "No classifications"
        return ", ".join(str(c) for c in self.classifications)

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"SutraTypeInfo(classifications={self.classifications})"


@dataclass
class PadaAnalysis:
    """
    Represents the grammatical analysis of a single word (pada).

    Attributes:
        word: The word in Sanskrit
        gender: Gender marker (usually 'S' for masculine, 'F' for feminine, 'N' for neuter)
        vibhakti: Case ending (1-8 or 0 for avyaya/indeclinable)
        vachana: Number (1-3 or 0 for avyaya/indeclinable)
    """

    word: str
    gender: str
    vibhakti: int  # 0-8, where 0 means avyaya/indeclinable
    vachana: int  # 0-3, where 0 means avyaya/indeclinable

    def __post_init__(self):
        """Validate the grammatical information."""
        if not (0 <= self.vibhakti <= 8):
            raise ValueError(f"Vibhakti must be between 0 and 8, got {self.vibhakti}")
        if not (0 <= self.vachana <= 3):
            raise ValueError(f"Vachana must be between 0 and 3, got {self.vachana}")
        # Both vibhakti and vachana should be 0 together for avyaya
        if (self.vibhakti == 0) != (self.vachana == 0):
            raise ValueError(
                "For avyaya/indeclinable words, both vibhakti and vachana must be 0"
            )

    @property
    def is_avyaya(self) -> bool:
        """Return True if this word is avyaya (indeclinable)."""
        return self.vibhakti == 0 and self.vachana == 0

    @property
    def vibhakti_name(self) -> str:
        """Return the name of the vibhakti."""
        vibhakti_names = {
            0: "Avyaya",
            1: "Prathama",
            2: "Dvitiya",
            3: "Tritiya",
            4: "Chaturthi",
            5: "Panchami",
            6: "Shashthi",
            7: "Saptami",
            8: "Sambodhana",
        }
        return vibhakti_names.get(self.vibhakti, "Unknown")

    @property
    def vachana_name(self) -> str:
        """Return the name of the vachana."""
        vachana_names = {
            0: "Avyaya",
            1: "Ekavachana",
            2: "Dvivachana",
            3: "Bahuvachana",
        }
        return vachana_names.get(self.vachana, "Unknown")

    def __str__(self) -> str:
        """Return a readable string representation."""
        if self.is_avyaya:
            return f"{self.word} (Avyaya)"
        return f"{self.word} ({self.vibhakti_name}, {self.vachana_name})"

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"PadaAnalysis(word='{self.word}', gender='{self.gender}', vibhakti={self.vibhakti}, vachana={self.vachana})"


@dataclass
class PadaVibhaga:
    """
    Represents the complete grammatical analysis (pada_vibhaga) of a sutra.

    Attributes:
        words: List of PadaAnalysis objects for each word in the sutra
    """

    words: List[PadaAnalysis]

    def __len__(self) -> int:
        """Return the number of words analyzed."""
        return len(self.words)

    def __iter__(self):
        """Allow iteration over word analyses."""
        return iter(self.words)

    def __getitem__(self, index) -> PadaAnalysis:
        """Allow indexing into the word analyses."""
        return self.words[index]

    @classmethod
    def from_string(cls, pc_string: str) -> "PadaVibhaga":
        """
        Parse a pada_vibhaga string into a PadaVibhaga object.

        Format: word1$gender$vibhakti$vachana$##word2$gender$vibhakti$vachana$##...

        Args:
            pc_string: The pada_vibhaga string from the data

        Returns:
            PadaVibhaga object with parsed word analyses
        """
        if not pc_string or pc_string.strip() == "":
            return cls([])

        words = []
        # Split by ## to get individual word analyses
        word_parts = pc_string.split("##")

        for part in word_parts:
            if not part.strip():
                continue

            # Split by $ to get word, gender, vibhakti, vachana
            components = part.split("$")
            if len(components) >= 4:
                word = components[0]
                gender = components[1]
                try:
                    vibhakti = int(components[2])
                    vachana = int(components[3])
                    analysis = PadaAnalysis(
                        word=word, gender=gender, vibhakti=vibhakti, vachana=vachana
                    )
                    words.append(analysis)
                except (ValueError, IndexError):
                    # Skip invalid entries
                    continue

        return cls(words)

    def __str__(self) -> str:
        """Return a readable string representation."""
        return f"PadaVibhaga({len(self.words)} words: {', '.join(str(w) for w in self.words)})"

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"PadaVibhaga(words={self.words})"


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
        pada_vibhaga: Grammatical analysis of the sutra words (PadaVibhaga object)
        sutra_type_info: Type classifications of the sutra (SutraTypeInfo object)
        an: Anuvrutti (continuation from previous sutras)
        ad: Additional data
        ss: Sanskrit with sandhi
    """

    identifier: SutraIdentifier
    text: SutraText
    references: SutraReferences
    pada_vibhaga: Optional[PadaVibhaga]  # Grammatical analysis
    sutra_type_info: SutraTypeInfo  # Type classifications of the sutra
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
