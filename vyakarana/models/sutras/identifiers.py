"""
Identifier classes for Sanskrit Grammar (Vyakarana) entities.

This module defines classes for identifying and referencing sutras.
"""

from dataclasses import dataclass


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
        if not 1 <= self.adhyaya <= 8:
            raise ValueError(f"Adhyaya must be between 1 and 8, got {self.adhyaya}")
        if not 1 <= self.pada <= 4:
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

    def __eq__(self, other) -> bool:
        """Check equality based on adhyaya, pada, and number."""
        if not isinstance(other, SutraIdentifier):
            return False
        return (self.adhyaya, self.pada, self.number) == (
            other.adhyaya,
            other.pada,
            other.number,
        )

    def __lt__(self, other) -> bool:
        """Compare ordering based on (adhyaya, pada, number) tuple."""
        if not isinstance(other, SutraIdentifier):
            return NotImplemented
        return (self.adhyaya, self.pada, self.number) < (
            other.adhyaya,
            other.pada,
            other.number,
        )

    def __le__(self, other) -> bool:
        """Less than or equal comparison."""
        if not isinstance(other, SutraIdentifier):
            return NotImplemented
        return (self.adhyaya, self.pada, self.number) <= (
            other.adhyaya,
            other.pada,
            other.number,
        )

    def __gt__(self, other) -> bool:
        """Greater than comparison."""
        if not isinstance(other, SutraIdentifier):
            return NotImplemented
        return (self.adhyaya, self.pada, self.number) > (
            other.adhyaya,
            other.pada,
            other.number,
        )

    def __ge__(self, other) -> bool:
        """Greater than or equal comparison."""
        if not isinstance(other, SutraIdentifier):
            return NotImplemented
        return (self.adhyaya, self.pada, self.number) >= (
            other.adhyaya,
            other.pada,
            other.number,
        )

    def __hash__(self) -> int:
        """Return hash value for use in sets and dictionaries."""
        return hash((self.adhyaya, self.pada, self.number))


@dataclass
class SutraReference:
    """
    Represents a reference to a specific sutra.

    Attributes:
        sutra_id: The identifier of the referenced sutra (SutraIdentifier object)
        text_portion: The specific text or words taken from the referenced sutra
    """

    sutra_id: SutraIdentifier
    text_portion: str

    @property
    def reference_string(self) -> str:
        """Return the reference as a formatted string like '1.1.1'."""
        return self.sutra_id.reference

    def __str__(self) -> str:
        """Return a readable string representation."""
        return f"{self.reference_string}: '{self.text_portion}'"

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"SutraReference(sutra_id={self.sutra_id}, text_portion='{self.text_portion}')"
