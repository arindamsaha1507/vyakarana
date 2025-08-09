"""
Grammatical analysis models for Sanskrit Grammar (Vyakarana) entities.

This module defines classes for representing grammatical analysis of Sanskrit words.
"""

from dataclasses import dataclass
from typing import List


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
        if not 0 <= self.vibhakti <= 8:
            raise ValueError(f"Vibhakti must be between 0 and 8, got {self.vibhakti}")
        if not 0 <= self.vachana <= 3:
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
        return (
            f"PadaAnalysis(word='{self.word}', gender='{self.gender}', "
            f"vibhakti={self.vibhakti}, vachana={self.vachana})"
        )


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

    def __getitem__(self, index: int) -> PadaAnalysis:
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
