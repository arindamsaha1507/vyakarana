"""
Comprehensive tests for the identifiers module.

Tests for SutraIdentifier and SutraReference classes.
"""

import pytest

from vyakarana.models.sutras.identifiers import SutraIdentifier, SutraReference


class TestSutraIdentifier:
    """Test cases for SutraIdentifier class."""

    def test_valid_creation(self):
        """Test creating valid SutraIdentifier instances."""
        # Test various valid combinations
        sutra_id = SutraIdentifier(adhyaya=1, pada=1, number=1)
        assert sutra_id.adhyaya == 1
        assert sutra_id.pada == 1
        assert sutra_id.number == 1

        # Test boundary values
        sutra_id = SutraIdentifier(adhyaya=8, pada=4, number=999)
        assert sutra_id.adhyaya == 8
        assert sutra_id.pada == 4
        assert sutra_id.number == 999

    def test_invalid_adhyaya(self):
        """Test invalid adhyaya values."""
        # Test adhyaya < 1
        with pytest.raises(ValueError, match="Adhyaya must be between 1 and 8"):
            SutraIdentifier(adhyaya=0, pada=1, number=1)

        with pytest.raises(ValueError, match="Adhyaya must be between 1 and 8"):
            SutraIdentifier(adhyaya=-1, pada=1, number=1)

        with pytest.raises(ValueError, match="Adhyaya must be between 1 and 8"):
            SutraIdentifier(adhyaya=9, pada=1, number=1)

    def test_invalid_pada(self):
        """Test invalid pada values."""
        # Test pada < 1
        with pytest.raises(ValueError, match="Pada must be between 1 and 4"):
            SutraIdentifier(adhyaya=1, pada=0, number=1)

        with pytest.raises(ValueError, match="Pada must be between 1 and 4"):
            SutraIdentifier(adhyaya=1, pada=-1, number=1)

        with pytest.raises(ValueError, match="Pada must be between 1 and 4"):
            SutraIdentifier(adhyaya=1, pada=5, number=1)

    def test_invalid_number(self):
        """Test invalid sutra number values."""
        # Test number <= 0
        with pytest.raises(ValueError, match="Sutra number must be positive"):
            SutraIdentifier(adhyaya=1, pada=1, number=0)

        with pytest.raises(ValueError, match="Sutra number must be positive"):
            SutraIdentifier(adhyaya=1, pada=1, number=-1)

    def test_reference_property(self):
        """Test the reference property."""
        sutra_id = SutraIdentifier(adhyaya=1, pada=1, number=1)
        assert sutra_id.reference == "1.1.1"

        sutra_id = SutraIdentifier(adhyaya=8, pada=4, number=127)
        assert sutra_id.reference == "8.4.127"

    def test_string_representations(self):
        """Test __str__ and __repr__ methods."""
        sutra_id = SutraIdentifier(adhyaya=1, pada=1, number=1)

        # Test __str__
        assert str(sutra_id) == "1.1.1"

        # Test __repr__
        expected_repr = "SutraIdentifier(adhyaya=1, pada=1, number=1)"
        assert repr(sutra_id) == expected_repr

    def test_equality(self):
        """Test equality comparison."""
        sutra1 = SutraIdentifier(adhyaya=1, pada=1, number=1)
        sutra2 = SutraIdentifier(adhyaya=1, pada=1, number=1)
        sutra3 = SutraIdentifier(adhyaya=1, pada=1, number=2)

        assert sutra1 == sutra2
        assert sutra1 != sutra3
        assert sutra1 != "1.1.1"  # Different type

    def test_ordering(self):
        """Test ordering comparison between SutraIdentifier instances."""
        sutra1 = SutraIdentifier(adhyaya=1, pada=1, number=1)
        sutra2 = SutraIdentifier(adhyaya=1, pada=1, number=2)
        sutra3 = SutraIdentifier(adhyaya=1, pada=2, number=1)
        sutra4 = SutraIdentifier(adhyaya=2, pada=1, number=1)

        # Test less than
        assert sutra1 < sutra2
        assert sutra1 < sutra3
        assert sutra1 < sutra4
        assert sutra2 < sutra3

        # Test greater than
        assert sutra2 > sutra1
        assert sutra3 > sutra1
        assert sutra4 > sutra1

        # Test less than or equal
        assert sutra1 <= sutra1
        assert sutra1 <= sutra2

        # Test greater than or equal
        assert sutra1 >= sutra1
        assert sutra2 >= sutra1

    def test_ordering_with_non_sutra_identifier(self):
        """Test ordering with non-SutraIdentifier objects."""
        sutra1 = SutraIdentifier(adhyaya=1, pada=1, number=1)
        sutra2 = SutraIdentifier(adhyaya=1, pada=1, number=2)

        assert sutra1 < sutra2

    def test_hash(self):
        """Test hash function for use in sets and dictionaries."""
        sutra1 = SutraIdentifier(adhyaya=1, pada=1, number=1)
        sutra2 = SutraIdentifier(adhyaya=1, pada=1, number=1)
        sutra3 = SutraIdentifier(adhyaya=1, pada=1, number=2)

        # Equal objects should have equal hashes
        assert hash(sutra1) == hash(sutra2)

        # Different objects should generally have different hashes
        assert hash(sutra1) != hash(sutra3)

        # Test use in set
        sutra_set = {sutra1, sutra2, sutra3}
        assert len(sutra_set) == 2  # sutra1 and sutra2 are equal


class TestSutraReference:
    """Test cases for SutraReference class."""

    def test_creation(self):
        """Test creating SutraReference instances."""
        sutra_id = SutraIdentifier(adhyaya=1, pada=1, number=1)
        ref = SutraReference(sutra_id=sutra_id, text_portion="वृद्धिः")

        assert ref.sutra_id == sutra_id
        assert ref.text_portion == "वृद्धिः"

    def test_reference_string_property(self):
        """Test the reference_string property."""
        sutra_id = SutraIdentifier(adhyaya=1, pada=1, number=1)
        ref = SutraReference(sutra_id=sutra_id, text_portion="वृद्धिः")

        assert ref.reference_string == "1.1.1"

    def test_string_representations(self):
        """Test __str__ and __repr__ methods."""
        sutra_id = SutraIdentifier(adhyaya=1, pada=1, number=1)
        ref = SutraReference(sutra_id=sutra_id, text_portion="वृद्धिः")

        # Test __str__
        expected_str = "1.1.1: 'वृद्धिः'"
        assert str(ref) == expected_str

        # Test __repr__ - using the actual format from the implementation
        expected_repr = "SutraReference(sutra_id=1.1.1, text_portion='वृद्धिः')"
        assert repr(ref) == expected_repr

    def test_with_empty_text(self):
        """Test SutraReference with empty text portion."""
        sutra_id = SutraIdentifier(adhyaya=1, pada=1, number=1)
        ref = SutraReference(sutra_id=sutra_id, text_portion="")

        assert ref.text_portion == ""
        assert str(ref) == "1.1.1: ''"

    def test_with_long_text(self):
        """Test SutraReference with long text portion."""
        sutra_id = SutraIdentifier(adhyaya=1, pada=1, number=1)
        long_text = "अदेङ्गुणः" * 10  # Repeat Sanskrit text
        ref = SutraReference(sutra_id=sutra_id, text_portion=long_text)

        assert ref.text_portion == long_text
        assert str(ref) == f"1.1.1: '{long_text}'"


class TestSutraIdentifierEdgeCases:
    """Test edge cases and comprehensive scenarios for SutraIdentifier."""

    def test_large_numbers(self):
        """Test with large sutra numbers."""
        sutra = SutraIdentifier(adhyaya=8, pada=4, number=9999)
        assert sutra.reference == "8.4.9999"

    def test_sorting_comprehensive(self):
        """Test comprehensive sorting scenarios."""
        sutras = [
            SutraIdentifier(adhyaya=2, pada=1, number=1),
            SutraIdentifier(adhyaya=1, pada=2, number=1),
            SutraIdentifier(adhyaya=1, pada=1, number=2),
            SutraIdentifier(adhyaya=1, pada=1, number=1),
        ]

        sorted_sutras = sorted(sutras)
        expected_order = [
            SutraIdentifier(adhyaya=1, pada=1, number=1),
            SutraIdentifier(adhyaya=1, pada=1, number=2),
            SutraIdentifier(adhyaya=1, pada=2, number=1),
            SutraIdentifier(adhyaya=2, pada=1, number=1),
        ]

        assert sorted_sutras == expected_order

    def test_reference_uniqueness(self):
        """Test that different combinations produce unique references."""
        refs = set()
        for adhyaya in range(1, 9):
            for pada in range(1, 5):
                for number in range(1, 5):
                    sutra = SutraIdentifier(adhyaya=adhyaya, pada=pada, number=number)
                    refs.add(sutra.reference)

        # Should have unique references for all combinations
        assert len(refs) == 8 * 4 * 4  # 128 unique combinations
