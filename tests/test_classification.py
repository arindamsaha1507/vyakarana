"""
Comprehensive tests for the classification module.

Tests for SutraTypeClassification and SutraTypeInfo classes.
"""

from vyakarana.models.sutras.classification import (
    SutraTypeClassification,
    SutraTypeInfo,
)
from vyakarana.models.sutras.enums import SutraType


class TestSutraTypeClassification:
    """Test cases for SutraTypeClassification class."""

    def test_creation_with_explanation(self):
        """Test creating SutraTypeClassification with explanation."""
        classification = SutraTypeClassification(
            sutra_type=SutraType.PARIBHASHA, explanation="व्यपदेशिवद्भावज्ञापकपरिभाषा"
        )

        assert classification.sutra_type == SutraType.PARIBHASHA
        assert classification.explanation == "व्यपदेशिवद्भावज्ञापकपरिभाषा"

    def test_creation_without_explanation(self):
        """Test creating SutraTypeClassification without explanation."""
        classification = SutraTypeClassification(sutra_type=SutraType.VIDHI)

        assert classification.sutra_type == SutraType.VIDHI
        assert classification.explanation is None

    def test_string_representation_with_explanation(self):
        """Test __str__ method with explanation."""
        classification = SutraTypeClassification(
            sutra_type=SutraType.ATIDESHA, explanation="आद्यन्तवदतिदेशः"
        )

        expected = "ATIDESHA (आद्यन्तवदतिदेशः)"
        assert str(classification) == expected

    def test_string_representation_without_explanation(self):
        """Test __str__ method without explanation."""
        classification = SutraTypeClassification(sutra_type=SutraType.SANJNA)

        assert str(classification) == "SANJNA"

    def test_repr_representation(self):
        """Test __repr__ method."""
        classification = SutraTypeClassification(
            sutra_type=SutraType.PARIBHASHA, explanation="test explanation"
        )

        expected = "SutraTypeClassification(sutra_type=SutraType.PARIBHASHA, explanation='test explanation')"
        assert repr(classification) == expected

    def test_repr_without_explanation(self):
        """Test __repr__ method without explanation."""
        classification = SutraTypeClassification(sutra_type=SutraType.VIDHI)

        expected = (
            "SutraTypeClassification(sutra_type=SutraType.VIDHI, explanation='None')"
        )
        assert repr(classification) == expected


class TestSutraTypeInfo:
    """Test cases for SutraTypeInfo class."""

    def test_creation_with_classifications(self):
        """Test creating SutraTypeInfo with classifications."""
        classifications = [
            SutraTypeClassification(SutraType.PARIBHASHA, "explanation1"),
            SutraTypeClassification(SutraType.VIDHI, "explanation2"),
        ]

        info = SutraTypeInfo(classifications=classifications)
        assert len(info.classifications) == 2
        assert info.classifications[0].sutra_type == SutraType.PARIBHASHA
        assert info.classifications[1].sutra_type == SutraType.VIDHI

    def test_creation_empty(self):
        """Test creating empty SutraTypeInfo."""
        info = SutraTypeInfo(classifications=[])
        assert len(info.classifications) == 0

    def test_len_method(self):
        """Test __len__ method."""
        classifications = [
            SutraTypeClassification(SutraType.PARIBHASHA),
            SutraTypeClassification(SutraType.VIDHI),
            SutraTypeClassification(SutraType.SANJNA),
        ]

        info = SutraTypeInfo(classifications=classifications)
        assert len(info) == 3

        empty_info = SutraTypeInfo(classifications=[])
        assert len(empty_info) == 0

    def test_iteration(self):
        """Test iteration over classifications."""
        classifications = [
            SutraTypeClassification(SutraType.PARIBHASHA),
            SutraTypeClassification(SutraType.VIDHI),
        ]

        info = SutraTypeInfo(classifications=classifications)

        collected = list(info)
        assert len(collected) == 2
        assert collected[0].sutra_type == SutraType.PARIBHASHA
        assert collected[1].sutra_type == SutraType.VIDHI

    def test_indexing(self):
        """Test indexing into classifications."""
        classifications = [
            SutraTypeClassification(SutraType.PARIBHASHA),
            SutraTypeClassification(SutraType.VIDHI),
            SutraTypeClassification(SutraType.SANJNA),
        ]

        info = SutraTypeInfo(classifications=classifications)

        assert info[0].sutra_type == SutraType.PARIBHASHA
        assert info[1].sutra_type == SutraType.VIDHI
        assert info[2].sutra_type == SutraType.SANJNA

        # Test negative indexing
        assert info[-1].sutra_type == SutraType.SANJNA

    def test_types_property(self):
        """Test the types property."""
        classifications = [
            SutraTypeClassification(SutraType.PARIBHASHA),
            SutraTypeClassification(SutraType.VIDHI),
            SutraTypeClassification(SutraType.ATIDESHA),
        ]

        info = SutraTypeInfo(classifications=classifications)
        types = info.types

        assert len(types) == 3
        assert SutraType.PARIBHASHA in types
        assert SutraType.VIDHI in types
        assert SutraType.ATIDESHA in types

    def test_from_string_valid(self):
        """Test from_string class method with valid input."""
        type_string = "P$व्यपदेशिवद्भावज्ञापकपरिभाषा$##AT$आद्यन्तवदतिदेशः$"

        info = SutraTypeInfo.from_string(type_string)

        assert len(info) == 2
        assert info[0].sutra_type == SutraType.PARIBHASHA
        assert info[0].explanation == "व्यपदेशिवद्भावज्ञापकपरिभाषा"
        assert info[1].sutra_type == SutraType.ATIDESHA
        assert info[1].explanation == "आद्यन्तवदतिदेशः"

    def test_from_string_without_explanations(self):
        """Test from_string with types but no explanations."""
        type_string = "P$##V$##S$"

        info = SutraTypeInfo.from_string(type_string)

        assert len(info) == 3
        assert info[0].sutra_type == SutraType.PARIBHASHA
        assert info[0].explanation is None
        assert info[1].sutra_type == SutraType.VIDHI
        assert info[1].explanation is None
        assert info[2].sutra_type == SutraType.SANJNA
        assert info[2].explanation is None

    def test_from_string_mixed_explanations(self):
        """Test from_string with some explanations and some without."""
        type_string = "P$explanation$##V$##S$another explanation$"

        info = SutraTypeInfo.from_string(type_string)

        assert len(info) == 3
        assert info[0].explanation == "explanation"
        assert info[1].explanation is None
        assert info[2].explanation == "another explanation"

    def test_from_string_empty(self):
        """Test from_string with empty string."""
        info = SutraTypeInfo.from_string("")
        assert len(info) == 0

        info = SutraTypeInfo.from_string("   ")
        assert len(info) == 0

    def test_from_string_invalid_types(self):
        """Test from_string with invalid type identifiers."""
        type_string = "INVALID$explanation$##P$valid$##ANOTHER_INVALID$bad$"

        info = SutraTypeInfo.from_string(type_string)

        # Should only include the valid type
        assert len(info) == 1
        assert info[0].sutra_type == SutraType.PARIBHASHA
        assert info[0].explanation == "valid"

    def test_from_string_malformed(self):
        """Test from_string with malformed input."""
        # Test with just separators
        info = SutraTypeInfo.from_string("##$$##")
        assert len(info) == 0

        # Test with empty parts
        info = SutraTypeInfo.from_string("P$explanation$####V$another$")
        assert len(info) == 2

    def test_str_representation(self):
        """Test __str__ method."""
        classifications = [
            SutraTypeClassification(SutraType.PARIBHASHA, "explanation1"),
            SutraTypeClassification(SutraType.VIDHI),
        ]

        info = SutraTypeInfo(classifications=classifications)

        expected = "PARIBHASHA (explanation1), VIDHI"
        assert str(info) == expected

    def test_str_representation_empty(self):
        """Test __str__ method with empty classifications."""
        info = SutraTypeInfo(classifications=[])
        assert str(info) == "No classifications"

    def test_repr_representation(self):
        """Test __repr__ method."""
        classifications = [SutraTypeClassification(SutraType.PARIBHASHA, "test")]

        info = SutraTypeInfo(classifications=classifications)

        expected = f"SutraTypeInfo(classifications={classifications})"
        assert repr(info) == expected


class TestSutraTypeInfoComplexScenarios:
    """Test complex scenarios and edge cases."""

    def test_duplicate_types(self):
        """Test handling duplicate types in classifications."""
        classifications = [
            SutraTypeClassification(SutraType.PARIBHASHA, "first"),
            SutraTypeClassification(SutraType.PARIBHASHA, "second"),
        ]

        info = SutraTypeInfo(classifications=classifications)

        assert len(info) == 2
        assert len(info.types) == 2  # Both instances should be in types list
        assert info.types.count(SutraType.PARIBHASHA) == 2

    def test_all_sutra_types(self):
        """Test with all available sutra types."""
        all_types = [
            SutraType.ADHIKARA,
            SutraType.VIDHI,
            SutraType.SANJNA,
            SutraType.PARIBHASHA,
            SutraType.ATIDESHA,
        ]

        classifications = [SutraTypeClassification(st) for st in all_types]
        info = SutraTypeInfo(classifications=classifications)

        assert len(info) == len(all_types)
        assert set(info.types) == set(all_types)

    def test_long_explanations(self):
        """Test with very long explanations."""
        long_explanation = "a" * 1000  # Very long explanation

        classification = SutraTypeClassification(SutraType.PARIBHASHA, long_explanation)

        info = SutraTypeInfo(classifications=[classification])

        assert info[0].explanation == long_explanation
        assert long_explanation in str(info)

    def test_special_characters_in_explanations(self):
        """Test with special characters in explanations."""
        special_explanation = "test$##with$special##chars$"

        classification = SutraTypeClassification(SutraType.VIDHI, special_explanation)

        info = SutraTypeInfo(classifications=[classification])
        assert info[0].explanation == special_explanation
