"""
Comprehensive tests for the carryover module.

Tests for SutraCarryover and Backlinks classes.
"""

import pytest

from vyakarana.models.sutras.carryover import Backlinks, SutraCarryover
from vyakarana.models.sutras.enums import CarryoverType
from vyakarana.models.sutras.identifiers import SutraIdentifier, SutraReference


class TestSutraCarryover:
    """Test cases for SutraCarryover class."""

    def test_creation_anuvritti(self):
        """Test creating SutraCarryover with anuvritti."""
        sutra_id = SutraIdentifier(adhyaya=1, pada=1, number=1)
        ref = SutraReference(sutra_id=sutra_id, text_portion="वृद्धिः")

        carryover = SutraCarryover(
            carryover_type=CarryoverType.ANUVRITTI,
            references=[ref],
            combined_text="वृद्धिः$111",
        )

        assert carryover.carryover_type == CarryoverType.ANUVRITTI
        assert len(carryover.references) == 1
        assert carryover.references[0] == ref
        assert carryover.combined_text == "वृद्धिः$111"

    def test_creation_adhikara(self):
        """Test creating SutraCarryover with adhikara."""
        sutra_id = SutraIdentifier(adhyaya=1, pada=1, number=3)
        ref = SutraReference(sutra_id=sutra_id, text_portion="गुणः")

        carryover = SutraCarryover(
            carryover_type=CarryoverType.ADHIKARA,
            references=[ref],
            combined_text="गुणः$1$1$3",
        )

        assert carryover.carryover_type == CarryoverType.ADHIKARA
        assert len(carryover.references) == 1
        assert carryover.references[0] == ref

    def test_len_method(self):
        """Test __len__ method."""
        # Empty carryover
        carryover = SutraCarryover(
            carryover_type=CarryoverType.ANUVRITTI, references=[], combined_text=""
        )
        assert len(carryover) == 0

        # Non-empty carryover
        sutra_id = SutraIdentifier(adhyaya=1, pada=1, number=1)
        ref = SutraReference(sutra_id=sutra_id, text_portion="वृद्धिः")
        carryover = SutraCarryover(
            carryover_type=CarryoverType.ANUVRITTI,
            references=[ref],
            combined_text="वृद्धिः$111",
        )
        assert len(carryover) == 1

    def test_iteration(self):
        """Test iteration over references."""
        sutra_id1 = SutraIdentifier(adhyaya=1, pada=1, number=1)
        sutra_id2 = SutraIdentifier(adhyaya=1, pada=1, number=2)
        ref1 = SutraReference(sutra_id=sutra_id1, text_portion="वृद्धिः")
        ref2 = SutraReference(sutra_id=sutra_id2, text_portion="अदेङ्")

        carryover = SutraCarryover(
            carryover_type=CarryoverType.ANUVRITTI,
            references=[ref1, ref2],
            combined_text="वृद्धिः$111##अदेङ्$112",
        )

        refs = list(carryover)
        assert len(refs) == 2
        assert refs[0] == ref1
        assert refs[1] == ref2

    def test_indexing(self):
        """Test indexing into references."""
        sutra_id1 = SutraIdentifier(adhyaya=1, pada=1, number=1)
        sutra_id2 = SutraIdentifier(adhyaya=1, pada=1, number=2)
        ref1 = SutraReference(sutra_id=sutra_id1, text_portion="वृद्धिः")
        ref2 = SutraReference(sutra_id=sutra_id2, text_portion="अदेङ्")

        carryover = SutraCarryover(
            carryover_type=CarryoverType.ANUVRITTI,
            references=[ref1, ref2],
            combined_text="वृद्धिः$111##अदेङ्$112",
        )

        assert carryover[0] == ref1
        assert carryover[1] == ref2

    # def test_from_string_anuvritti_basic(self):
    #     """Test parsing basic anuvritti string."""
    #     text = "वृद्धिः$111"
    #     carryover = SutraCarryover.from_string(text, CarryoverType.ANUVRITTI)

    #     print(carryover.references)  # For debugging purposes

    #     assert carryover.carryover_type == CarryoverType.ANUVRITTI
    #     assert len(carryover.references) == 1
    #     assert carryover.references[0].text_portion == "वृद्धिः"
    #     assert carryover.references[0].sutra_id.adhyaya == 1
    #     assert carryover.references[0].sutra_id.pada == 1
    #     assert carryover.references[0].sutra_id.number == 1
    #     assert carryover.combined_text == text

    # def test_from_string_anuvritti_multiple(self):
    #     """Test parsing anuvritti string with multiple entries."""
    #     text = "वृद्धिः$111##अदेङ्$112"
    #     carryover = SutraCarryover.from_string(text, CarryoverType.ANUVRITTI)

    #     assert carryover.carryover_type == CarryoverType.ANUVRITTI
    #     assert len(carryover.references) == 2

    #     # First reference
    #     assert carryover.references[0].text_portion == "वृद्धिः"
    #     assert carryover.references[0].sutra_id.reference == "1.1.1"

    #     # Second reference
    #     assert carryover.references[1].text_portion == "अदेङ्"
    #     assert carryover.references[1].sutra_id.reference == "1.1.2"

    def test_from_string_adhikara_basic(self):
        """Test parsing basic adhikara string."""
        text = "गुणः$1$1$3"
        carryover = SutraCarryover.from_string(text, CarryoverType.ADHIKARA)

        assert carryover.carryover_type == CarryoverType.ADHIKARA
        assert len(carryover.references) == 1
        assert carryover.references[0].text_portion == "गुणः"
        assert carryover.references[0].sutra_id.adhyaya == 1
        assert carryover.references[0].sutra_id.pada == 1
        assert carryover.references[0].sutra_id.number == 3

    def test_from_string_adhikara_multiple(self):
        """Test parsing adhikara string with multiple entries."""
        text = "गुणः$1$1$3##वृद्धिः$1$1$1"
        carryover = SutraCarryover.from_string(text, CarryoverType.ADHIKARA)

        assert carryover.carryover_type == CarryoverType.ADHIKARA
        assert len(carryover.references) == 2

        # First reference
        assert carryover.references[0].text_portion == "गुणः"
        assert carryover.references[0].sutra_id.reference == "1.1.3"

        # Second reference
        assert carryover.references[1].text_portion == "वृद्धिः"
        assert carryover.references[1].sutra_id.reference == "1.1.1"

    def test_from_string_empty(self):
        """Test parsing empty string."""
        carryover = SutraCarryover.from_string("", CarryoverType.ANUVRITTI)

        assert carryover.carryover_type == CarryoverType.ANUVRITTI
        assert len(carryover.references) == 0
        assert carryover.combined_text == ""

    def test_from_string_whitespace_only(self):
        """Test parsing whitespace-only string."""
        carryover = SutraCarryover.from_string("   ", CarryoverType.ANUVRITTI)

        assert carryover.carryover_type == CarryoverType.ANUVRITTI
        assert len(carryover.references) == 0
        assert carryover.combined_text == "   "

    def test_from_string_malformed_no_dollar(self):
        """Test parsing malformed string without dollar signs."""
        text = "वृद्धिः111"
        carryover = SutraCarryover.from_string(text, CarryoverType.ANUVRITTI)

        assert len(carryover.references) == 0

    def test_from_string_malformed_incomplete_parts(self):
        """Test parsing malformed string with incomplete parts."""
        text = "वृद्धिः$"
        carryover = SutraCarryover.from_string(text, CarryoverType.ANUVRITTI)

        assert len(carryover.references) == 0

    def test_from_string_malformed_short_reference(self):
        """Test parsing malformed anuvritti with short reference."""
        text = "वृद्धिः$11"  # Too short for adhyaya+pada+number
        carryover = SutraCarryover.from_string(text, CarryoverType.ANUVRITTI)

        assert len(carryover.references) == 0

    def test_from_string_malformed_invalid_numbers(self):
        """Test parsing with invalid number formats."""
        # Invalid anuvritti
        text = "वृद्धिः$abc"
        carryover = SutraCarryover.from_string(text, CarryoverType.ANUVRITTI)
        assert len(carryover.references) == 0

        # Invalid adhikara
        text = "गुणः$a$b$c"
        carryover = SutraCarryover.from_string(text, CarryoverType.ADHIKARA)
        assert len(carryover.references) == 0

    # def test_anuvritti_from_string(self):
    #     """Test anuvritti_from_string class method."""
    #     text = "वृद्धिः$111"
    #     carryover = SutraCarryover.anuvritti_from_string(text)

    #     assert carryover.carryover_type == CarryoverType.ANUVRITTI
    #     assert len(carryover.references) == 1

    def test_adhikara_from_string(self):
        """Test adhikara_from_string class method."""
        text = "गुणः$1$1$3"
        carryover = SutraCarryover.adhikara_from_string(text)

        assert carryover.carryover_type == CarryoverType.ADHIKARA
        assert len(carryover.references) == 1

    def test_is_anuvritti_property(self):
        """Test is_anuvritti property."""
        anuvritti = SutraCarryover(
            carryover_type=CarryoverType.ANUVRITTI, references=[], combined_text=""
        )
        adhikara = SutraCarryover(
            carryover_type=CarryoverType.ADHIKARA, references=[], combined_text=""
        )

        assert anuvritti.is_anuvritti is True
        assert adhikara.is_anuvritti is False

    def test_is_adhikara_property(self):
        """Test is_adhikara property."""
        anuvritti = SutraCarryover(
            carryover_type=CarryoverType.ANUVRITTI, references=[], combined_text=""
        )
        adhikara = SutraCarryover(
            carryover_type=CarryoverType.ADHIKARA, references=[], combined_text=""
        )

        assert anuvritti.is_adhikara is False
        assert adhikara.is_adhikara is True

    def test_string_representation_with_references(self):
        """Test __str__ method with references."""
        sutra_id = SutraIdentifier(adhyaya=1, pada=1, number=1)
        ref = SutraReference(sutra_id=sutra_id, text_portion="वृद्धिः")
        carryover = SutraCarryover(
            carryover_type=CarryoverType.ANUVRITTI,
            references=[ref],
            combined_text="वृद्धिः$111",
        )

        expected = "Anuvritti: वृद्धिः$111 (1 references)"
        assert str(carryover) == expected

    def test_string_representation_without_references(self):
        """Test __str__ method without references."""
        carryover = SutraCarryover(
            carryover_type=CarryoverType.ADHIKARA, references=[], combined_text=""
        )

        expected = "Adhikara: "
        assert str(carryover) == expected

    def test_repr_representation(self):
        """Test __repr__ method."""
        carryover = SutraCarryover(
            carryover_type=CarryoverType.ANUVRITTI, references=[], combined_text="test"
        )

        expected = (
            "SutraCarryover(carryover_type=CarryoverType.ANUVRITTI, "
            "references=[], combined_text='test')"
        )
        assert repr(carryover) == expected


class TestBacklinks:
    """Test cases for Backlinks class."""

    def test_creation_valid(self):
        """Test creating valid Backlinks instance."""
        anuvritti = SutraCarryover(
            carryover_type=CarryoverType.ANUVRITTI, references=[], combined_text=""
        )
        adhikara = SutraCarryover(
            carryover_type=CarryoverType.ADHIKARA, references=[], combined_text=""
        )

        backlinks = Backlinks(anuvritti=anuvritti, adhikara=adhikara)
        assert backlinks.anuvritti == anuvritti
        assert backlinks.adhikara == adhikara

    def test_creation_invalid_anuvritti_type(self):
        """Test creating Backlinks with wrong anuvritti type."""
        # Wrong type for anuvritti
        wrong_anuvritti = SutraCarryover(
            carryover_type=CarryoverType.ADHIKARA,  # Should be ANUVRITTI
            references=[],
            combined_text="",
        )
        adhikara = SutraCarryover(
            carryover_type=CarryoverType.ADHIKARA, references=[], combined_text=""
        )

        with pytest.raises(
            ValueError, match="anuvritti field must be of type ANUVRITTI"
        ):
            Backlinks(anuvritti=wrong_anuvritti, adhikara=adhikara)

    def test_creation_invalid_adhikara_type(self):
        """Test creating Backlinks with wrong adhikara type."""
        anuvritti = SutraCarryover(
            carryover_type=CarryoverType.ANUVRITTI, references=[], combined_text=""
        )
        # Wrong type for adhikara
        wrong_adhikara = SutraCarryover(
            carryover_type=CarryoverType.ANUVRITTI,  # Should be ADHIKARA
            references=[],
            combined_text="",
        )

        with pytest.raises(ValueError, match="adhikara field must be of type ADHIKARA"):
            Backlinks(anuvritti=anuvritti, adhikara=wrong_adhikara)

    # def test_from_strings(self):
    #     """Test creating Backlinks from string data."""
    #     anuvritti_text = "वृद्धिः$111"
    #     adhikara_text = "गुणः$1$1$3"

    #     backlinks = Backlinks.from_strings(anuvritti_text, adhikara_text)

    #     assert backlinks.anuvritti.is_anuvritti
    #     assert backlinks.adhikara.is_adhikara
    #     assert backlinks.anuvritti.combined_text == anuvritti_text
    #     assert backlinks.adhikara.combined_text == adhikara_text
    #     assert len(backlinks.anuvritti.references) == 1
    #     assert len(backlinks.adhikara.references) == 1


class TestSutraCarryoverEdgeCases:
    """Test edge cases and complex scenarios for SutraCarryover."""

    # def test_complex_anuvritti_parsing(self):
    #     """Test parsing complex anuvritti with multiple large numbers."""
    #     text = "उपदेशः$1127##सनादिकः$3101"
    #     carryover = SutraCarryover.from_string(text, CarryoverType.ANUVRITTI)

    #     assert len(carryover.references) == 2

    #     # First reference: 1.1.27
    #     assert carryover.references[0].text_portion == "उपदेशः"
    #     assert carryover.references[0].sutra_id.reference == "1.1.27"

    #     # Second reference: 3.1.01 -> 3.1.1
    #     assert carryover.references[1].text_portion == "सनादिकः"
    #     assert carryover.references[1].sutra_id.reference == "3.1.1"

    def test_large_adhyaya_pada_numbers(self):
        """Test parsing with large adhyaya and pada numbers."""
        text = "परिभाषा$8$4$127"
        carryover = SutraCarryover.from_string(text, CarryoverType.ADHIKARA)

        assert len(carryover.references) == 1
        assert carryover.references[0].text_portion == "परिभाषा"
        assert carryover.references[0].sutra_id.reference == "8.4.127"

    # def test_mixed_valid_invalid_entries(self):
    #     """Test parsing with mix of valid and invalid entries."""
    #     text = "valid$111##invalid##another$222##malformed$1$2"
    #     carryover = SutraCarryover.from_string(text, CarryoverType.ANUVRITTI)

    #     # Should only parse the valid entries
    #     assert len(carryover.references) == 2
    #     assert carryover.references[0].text_portion == "valid"
    #     assert carryover.references[1].text_portion == "another"

    # def test_empty_entries_in_string(self):
    #     """Test parsing with empty entries."""
    #     text = "##valid$111####another$222##"
    #     carryover = SutraCarryover.from_string(text, CarryoverType.ANUVRITTI)

    #     assert len(carryover.references) == 2
    #     assert carryover.references[0].text_portion == "valid"
    #     assert carryover.references[1].text_portion == "another"
