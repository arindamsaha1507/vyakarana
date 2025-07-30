"""
Carryover models for Sanskrit Grammar (Vyakarana) entities.

This module defines classes for representing anuvritti and adhikara carryover from previous sutras.
"""

from dataclasses import dataclass
from typing import List

from vyakarana.models.enums import CarryoverType
from vyakarana.models.identifiers import SutraIdentifier, SutraReference


@dataclass
class SutraCarryover:
    """
    Represents carryover from previous sutras - both anuvritti and adhikara.

    Anuvritti refers to words or portions from previous sutras that continue to apply
    to the current sutra, even though they are not explicitly stated.

    Adhikara refers to governing rules that apply over a range of sutras until
    explicitly terminated or superseded.

    Attributes:
        carryover_type: Type of carryover (anuvritti or adhikara)
        references: List of references to previous sutras and their carried-over portions
        combined_text: The complete carryover text as it appears in the data
    """

    carryover_type: CarryoverType
    references: List[SutraReference]
    combined_text: str

    def __len__(self) -> int:
        """Return the number of sutra references."""
        return len(self.references)

    def __iter__(self):
        """Allow iteration over the references."""
        return iter(self.references)

    def __getitem__(self, index) -> SutraReference:
        """Allow indexing into the references."""
        return self.references[index]

    @classmethod
    def from_string(
        cls, carryover_text: str, carryover_type: CarryoverType
    ) -> "SutraCarryover":
        """
        Parse a carryover string into a SutraCarryover object.

        Args:
            carryover_text: The carryover string from the data
            carryover_type: The type of carryover (anuvritti or adhikara)

        Returns:
            SutraCarryover object with parsed references
        """
        references = []

        if not carryover_text or not carryover_text.strip():
            return cls(
                carryover_type=carryover_type,
                references=references,
                combined_text=carryover_text,
            )

        # Split by ## to get individual entries
        entries = carryover_text.split("##")

        for entry in entries:
            if "$" not in entry:
                continue

            # Split by $ to separate text from reference parts
            parts = entry.split("$")

            if len(parts) < 2:
                continue

            # First part is always the text
            text = parts[0].strip()

            if carryover_type == CarryoverType.ANUVRITTI:
                # Anuvritti format: text$reference_number
                if len(parts) == 2:
                    ref_str = parts[1].strip()
                    if len(ref_str) >= 5:  # Format: adhyaya(1)pada(1)number(3+)
                        try:
                            adhyaya = int(ref_str[0])
                            pada = int(ref_str[1])
                            number = int(ref_str[2:])

                            sutra_id = SutraIdentifier(
                                adhyaya=adhyaya, pada=pada, number=number
                            )
                            reference = SutraReference(
                                sutra_id=sutra_id, text_portion=text
                            )
                            references.append(reference)
                        except (ValueError, IndexError):
                            # Skip malformed references
                            continue

            elif carryover_type == CarryoverType.ADHIKARA:
                # Adhikara format: text$adhyaya$pada$number
                if len(parts) == 4:
                    try:
                        adhyaya = int(parts[1].strip())
                        pada = int(parts[2].strip())
                        number = int(parts[3].strip())

                        sutra_id = SutraIdentifier(
                            adhyaya=adhyaya, pada=pada, number=number
                        )
                        reference = SutraReference(sutra_id=sutra_id, text_portion=text)
                        references.append(reference)
                    except (ValueError, IndexError):
                        # Skip malformed references
                        continue

        return cls(
            carryover_type=carryover_type,
            references=references,
            combined_text=carryover_text,
        )

    @classmethod
    def anuvritti_from_string(cls, anuvritti_text: str) -> "SutraCarryover":
        """Create an anuvritti SutraCarryover from a string."""
        return cls.from_string(anuvritti_text, CarryoverType.ANUVRITTI)

    @classmethod
    def adhikara_from_string(cls, adhikara_text: str) -> "SutraCarryover":
        """Create an adhikara SutraCarryover from a string."""
        return cls.from_string(adhikara_text, CarryoverType.ADHIKARA)

    @property
    def is_anuvritti(self) -> bool:
        """Return True if this is anuvritti carryover."""
        return self.carryover_type == CarryoverType.ANUVRITTI

    @property
    def is_adhikara(self) -> bool:
        """Return True if this is adhikara carryover."""
        return self.carryover_type == CarryoverType.ADHIKARA

    def __str__(self) -> str:
        """Return a readable string representation."""
        if self.references:
            ref_str = f" ({len(self.references)} references)"
        else:
            ref_str = ""
        type_name = self.carryover_type.value.capitalize()
        return f"{type_name}: {self.combined_text}{ref_str}"

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return (
            f"SutraCarryover(carryover_type={self.carryover_type}, "
            f"references={self.references}, combined_text='{self.combined_text}')"
        )


@dataclass
class Backlinks:
    """
    Represents backlinks to previous sutras - containing both anuvritti and adhikara.

    This class groups together the two types of carryover from previous sutras:
    - Anuvritti: continuation/carryover of words/meanings from previous sutras
    - Adhikara: governing rules that apply over a range of sutras

    Attributes:
        anuvritti: Anuvritti carryover (continuation from previous sutras)
        adhikara: Adhikara carryover (governing rules from previous sutras)
    """

    anuvritti: SutraCarryover
    adhikara: SutraCarryover

    def __post_init__(self):
        """Validate that carryover types are correct."""
        if not self.anuvritti.is_anuvritti:
            raise ValueError("anuvritti field must be of type ANUVRITTI")
        if not self.adhikara.is_adhikara:
            raise ValueError("adhikara field must be of type ADHIKARA")

    @classmethod
    def from_strings(cls, anuvritti_text: str, adhikara_text: str) -> "Backlinks":
        """
        Create a Backlinks object from anuvritti and adhikara text strings.

        Args:
            anuvritti_text: The anuvritti string from the data
            adhikara_text: The adhikara string from the data

        Returns:
            Backlinks object
        """
        anuvritti = SutraCarryover.anuvritti_from_string(anuvritti_text)
        adhikara = SutraCarryover.adhikara_from_string(adhikara_text)
        return cls(anuvritti=anuvritti, adhikara=adhikara)

    @property
    def has_anuvritti(self) -> bool:
        """Return True if there is anuvritti content."""
        return bool(self.anuvritti.combined_text.strip())

    @property
    def has_adhikara(self) -> bool:
        """Return True if there is adhikara content."""
        return bool(self.adhikara.combined_text.strip())

    @property
    def has_any_carryover(self) -> bool:
        """Return True if there is any carryover content."""
        return self.has_anuvritti or self.has_adhikara

    @property
    def total_references(self) -> int:
        """Return the total number of references across both carryovers."""
        return len(self.anuvritti) + len(self.adhikara)

    def __str__(self) -> str:
        """Return a readable string representation."""
        parts = []
        if self.has_anuvritti:
            parts.append(f"Anuvritti: {self.anuvritti.combined_text[:50]}...")
        if self.has_adhikara:
            parts.append(f"Adhikara: {self.adhikara.combined_text[:50]}...")

        if not parts:
            return "Backlinks: No carryover"

        return f"Backlinks({', '.join(parts)})"

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"Backlinks(anuvritti={self.anuvritti!r}, adhikara={self.adhikara!r})"
