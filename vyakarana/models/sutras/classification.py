"""
Classification models for Sanskrit Grammar (Vyakarana) entities.

This module defines classes for representing sutra type classifications.
"""

from dataclasses import dataclass
from typing import List, Optional

from .enums import SutraType


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
        return (
            f"SutraTypeClassification(sutra_type={self.sutra_type}, "
            f"explanation='{self.explanation}')"
        )


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

    def __getitem__(self, index: int) -> SutraTypeClassification:
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
