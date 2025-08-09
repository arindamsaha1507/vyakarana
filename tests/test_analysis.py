"""
Comprehensive tests for the analysis module.

Tests for PadaAnalysis and PadaVibhaga classes.
"""

import pytest

from vyakarana.models.sutras.analysis import PadaAnalysis, PadaVibhaga


class TestPadaAnalysis:
    """Test cases for PadaAnalysis class."""

    def test_creation_complete(self):
        """Test creating PadaAnalysis with all fields."""
        analysis = PadaAnalysis(word="राम", gender="S", vibhakti=1, vachana=1)

        assert analysis.word == "राम"
        assert analysis.gender == "S"
        assert analysis.vibhakti == 1
        assert analysis.vachana == 1

    def test_creation_avyaya(self):
        """Test creating PadaAnalysis for avyaya (indeclinable) words."""
        analysis = PadaAnalysis(word="अथ", gender="A", vibhakti=0, vachana=0)

        assert analysis.word == "अथ"
        assert analysis.gender == "A"
        assert analysis.vibhakti == 0
        assert analysis.vachana == 0
        assert analysis.is_avyaya

    def test_invalid_vibhakti(self):
        """Test invalid vibhakti values."""

        with pytest.raises(ValueError, match="Vibhakti must be between 0 and 8"):
            PadaAnalysis(word="test", gender="S", vibhakti=9, vachana=1)

        with pytest.raises(ValueError, match="Vibhakti must be between 0 and 8"):
            PadaAnalysis(word="test", gender="S", vibhakti=-1, vachana=1)

    def test_invalid_vachana(self):
        """Test invalid vachana values."""

        with pytest.raises(ValueError, match="Vachana must be between 0 and 3"):
            PadaAnalysis(word="test", gender="S", vibhakti=1, vachana=4)

        with pytest.raises(ValueError, match="Vachana must be between 0 and 3"):
            PadaAnalysis(word="test", gender="S", vibhakti=1, vachana=-1)

    def test_invalid_avyaya_combination(self):
        """Test invalid combinations for avyaya words."""

        # vibhakti=0 but vachana!=0
        with pytest.raises(ValueError, match="both vibhakti and vachana must be 0"):
            PadaAnalysis(word="test", gender="A", vibhakti=0, vachana=1)

        # vachana=0 but vibhakti!=0
        with pytest.raises(ValueError, match="both vibhakti and vachana must be 0"):
            PadaAnalysis(word="test", gender="A", vibhakti=1, vachana=0)

    def test_is_avyaya_property(self):
        """Test the is_avyaya property."""
        avyaya = PadaAnalysis(word="अथ", gender="A", vibhakti=0, vachana=0)
        assert avyaya.is_avyaya

        non_avyaya = PadaAnalysis(word="राम", gender="S", vibhakti=1, vachana=1)
        assert not non_avyaya.is_avyaya

    def test_vibhakti_name_property(self):
        """Test the vibhakti_name property."""
        test_cases = [
            (0, "Avyaya"),
            (1, "Prathama"),
            (2, "Dvitiya"),
            (3, "Tritiya"),
            (4, "Chaturthi"),
            (5, "Panchami"),
            (6, "Shashthi"),
            (7, "Saptami"),
            (8, "Sambodhana"),
        ]

        for vibhakti_num, expected_name in test_cases:
            vachana = 0 if vibhakti_num == 0 else 1
            analysis = PadaAnalysis(
                word="test", gender="S", vibhakti=vibhakti_num, vachana=vachana
            )
            assert analysis.vibhakti_name == expected_name

    def test_vachana_name_property(self):
        """Test the vachana_name property."""
        test_cases = [
            (0, "Avyaya"),
            (1, "Ekavachana"),
            (2, "Dvivachana"),
            (3, "Bahuvachana"),
        ]

        for vachana_num, expected_name in test_cases:
            vibhakti = 0 if vachana_num == 0 else 1
            analysis = PadaAnalysis(
                word="test", gender="S", vibhakti=vibhakti, vachana=vachana_num
            )
            assert analysis.vachana_name == expected_name

    def test_string_representation_avyaya(self):
        """Test __str__ method for avyaya words."""
        analysis = PadaAnalysis(word="अथ", gender="A", vibhakti=0, vachana=0)
        expected = "अथ (Avyaya)"
        assert str(analysis) == expected

    def test_string_representation_normal(self):
        """Test __str__ method for normal words."""
        analysis = PadaAnalysis(word="रामस्य", gender="S", vibhakti=6, vachana=1)
        expected = "रामस्य (Shashthi, Ekavachana)"
        assert str(analysis) == expected

    def test_repr_representation(self):
        """Test __repr__ method."""
        analysis = PadaAnalysis(word="देव", gender="S", vibhakti=1, vachana=3)
        expected = "PadaAnalysis(word='देव', gender='S', vibhakti=1, vachana=3)"
        assert repr(analysis) == expected


class TestPadaVibhaga:
    """Test cases for PadaVibhaga class."""

    def test_creation_with_words(self):
        """Test creating PadaVibhaga with word analyses."""
        words = [PadaAnalysis("राम", "S", 1, 1), PadaAnalysis("गच्छति", "A", 0, 0)]

        vibhaga = PadaVibhaga(words=words)
        assert len(vibhaga.words) == 2
        assert vibhaga.words[0].word == "राम"
        assert vibhaga.words[1].word == "गच्छति"

    def test_creation_empty(self):
        """Test creating empty PadaVibhaga."""
        vibhaga = PadaVibhaga(words=[])
        assert len(vibhaga.words) == 0

    def test_len_method(self):
        """Test __len__ method."""
        words = [
            PadaAnalysis("राम", "S", 1, 1),
            PadaAnalysis("गच्छति", "A", 0, 0),
            PadaAnalysis("वन", "N", 2, 1),
        ]

        vibhaga = PadaVibhaga(words=words)
        assert len(vibhaga) == 3

        empty_vibhaga = PadaVibhaga(words=[])
        assert len(empty_vibhaga) == 0

    def test_iteration(self):
        """Test iteration over word analyses."""
        words = [PadaAnalysis("राम", "S", 1, 1), PadaAnalysis("गच्छति", "A", 0, 0)]

        vibhaga = PadaVibhaga(words=words)

        collected = list(vibhaga)
        assert len(collected) == 2
        assert collected[0].word == "राम"
        assert collected[1].word == "गच्छति"

    def test_indexing(self):
        """Test indexing into word analyses."""
        words = [
            PadaAnalysis("राम", "S", 1, 1),
            PadaAnalysis("गच्छति", "A", 0, 0),
            PadaAnalysis("वन", "N", 2, 1),
        ]

        vibhaga = PadaVibhaga(words=words)

        assert vibhaga[0].word == "राम"
        assert vibhaga[1].word == "गच्छति"
        assert vibhaga[2].word == "वन"

        # Test negative indexing
        assert vibhaga[-1].word == "वन"

    def test_from_string_basic(self):
        """Test from_string class method with basic input."""
        vibhaga_string = "राम$S$1$1##गच्छति$A$0$0"

        vibhaga = PadaVibhaga.from_string(vibhaga_string)

        assert len(vibhaga) == 2
        assert vibhaga[0].word == "राम"
        assert vibhaga[0].gender == "S"
        assert vibhaga[0].vibhakti == 1
        assert vibhaga[0].vachana == 1
        assert vibhaga[1].word == "गच्छति"
        assert vibhaga[1].gender == "A"
        assert vibhaga[1].vibhakti == 0
        assert vibhaga[1].vachana == 0

    def test_from_string_complex(self):
        """Test from_string with multiple words."""
        vibhaga_string = "रामस्य$S$6$1##गृहे$N$7$1##तिष्ठति$A$0$0"

        vibhaga = PadaVibhaga.from_string(vibhaga_string)

        assert len(vibhaga) == 3

        # First word
        assert vibhaga[0].word == "रामस्य"
        assert vibhaga[0].gender == "S"
        assert vibhaga[0].vibhakti == 6  # Shashthi
        assert vibhaga[0].vachana == 1  # Ekavachana

        # Second word
        assert vibhaga[1].word == "गृहे"
        assert vibhaga[1].gender == "N"
        assert vibhaga[1].vibhakti == 7  # Saptami
        assert vibhaga[1].vachana == 1  # Ekavachana

        # Third word
        assert vibhaga[2].word == "तिष्ठति"
        assert vibhaga[2].gender == "A"
        assert vibhaga[2].vibhakti == 0  # Avyaya
        assert vibhaga[2].vachana == 0  # Avyaya

    def test_from_string_empty(self):
        """Test from_string with empty string."""
        vibhaga = PadaVibhaga.from_string("")
        assert len(vibhaga) == 0

        vibhaga = PadaVibhaga.from_string("   ")
        assert len(vibhaga) == 0

    def test_from_string_malformed(self):
        """Test from_string with malformed input."""
        # Test with incomplete parts (missing components)
        vibhaga_string = "राम$S$1##गच्छति$A$0$0"
        vibhaga = PadaVibhaga.from_string(vibhaga_string)
        # Should skip malformed parts and only include valid ones
        assert len(vibhaga) == 1
        assert vibhaga[0].word == "गच्छति"

    def test_from_string_invalid_numbers(self):
        """Test from_string with invalid vibhakti/vachana values."""
        # Test with non-numeric vibhakti/vachana
        vibhaga_string = "राम$S$abc$1##गच्छति$A$0$0"
        vibhaga = PadaVibhaga.from_string(vibhaga_string)
        # Should skip invalid entries
        assert len(vibhaga) == 1
        assert vibhaga[0].word == "गच्छति"

    def test_from_string_invalid_avyaya_combination(self):
        """Test from_string with invalid avyaya combinations."""
        # This should fail validation during PadaAnalysis creation
        vibhaga_string = "राम$S$0$1"  # vibhakti=0 but vachana=1
        vibhaga = PadaVibhaga.from_string(vibhaga_string)
        # Should skip invalid entries
        assert len(vibhaga) == 0

    def test_string_representation(self):
        """Test __str__ method."""
        words = [PadaAnalysis("राम", "S", 1, 1), PadaAnalysis("गच्छति", "A", 0, 0)]

        vibhaga = PadaVibhaga(words=words)

        result = str(vibhaga)
        assert "PadaVibhaga(2 words:" in result
        assert "राम (Prathama, Ekavachana)" in result
        assert "गच्छति (Avyaya)" in result

    def test_repr_representation(self):
        """Test __repr__ method."""
        words = [PadaAnalysis("राम", "S", 1, 1)]

        vibhaga = PadaVibhaga(words=words)

        expected = f"PadaVibhaga(words={words})"
        assert repr(vibhaga) == expected


class TestPadaAnalysisEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_all_valid_vibhakti_values(self):
        """Test all valid vibhakti values (0-8)."""
        for vibhakti in range(9):  # 0 to 8
            vachana = 0 if vibhakti == 0 else 1
            analysis = PadaAnalysis(
                word=f"word{vibhakti}", gender="S", vibhakti=vibhakti, vachana=vachana
            )
            assert analysis.vibhakti == vibhakti

    def test_all_valid_vachana_values(self):
        """Test all valid vachana values (0-3)."""
        for vachana in range(4):  # 0 to 3
            vibhakti = 0 if vachana == 0 else 1
            analysis = PadaAnalysis(
                word=f"word{vachana}", gender="S", vibhakti=vibhakti, vachana=vachana
            )
            assert analysis.vachana == vachana

    def test_unicode_sanskrit_words(self):
        """Test with various Unicode Sanskrit characters."""
        sanskrit_words = ["कृष्णः", "गोविन्दो", "मुकुन्दो", "मुरारिः"]

        for word in sanskrit_words:
            analysis = PadaAnalysis(word=word, gender="S", vibhakti=1, vachana=1)
            assert analysis.word == word
            assert word in str(analysis)

    def test_gender_variations(self):
        """Test with different gender markers."""
        genders = ["S", "F", "N", "A"]  # Masculine, Feminine, Neuter, Avyaya

        for gender in genders:
            if gender == "A":
                analysis = PadaAnalysis(
                    word="test", gender=gender, vibhakti=0, vachana=0
                )
            else:
                analysis = PadaAnalysis(
                    word="test", gender=gender, vibhakti=1, vachana=1
                )
            assert analysis.gender == gender

    def test_large_vibhaga(self):
        """Test PadaVibhaga with many words."""
        words = []
        for i in range(50):
            words.append(PadaAnalysis(f"word{i}", "S", 1, 1))

        vibhaga = PadaVibhaga(words=words)
        assert len(vibhaga) == 50
        assert vibhaga[0].word == "word0"
        assert vibhaga[49].word == "word49"
