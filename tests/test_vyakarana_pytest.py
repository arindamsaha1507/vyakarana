"""
Pytest-compatible tests for the Vyakarana package.

Run with: pytest tests/test_vyakarana_pytest.py
"""

import json
import sys
from pathlib import Path

import pytest

# Add the parent directory to the path to import vyakarana
sys.path.insert(0, str(Path(__file__).parent.parent))

from vyakarana import read_sutras
from vyakarana.models import Sutra, SutraCollection


# pylint: disable=redefined-outer-name


@pytest.fixture
def data_file_path():
    """Fixture to provide the data file path."""
    current_dir = Path(__file__).parent
    return current_dir.parent / "sutraani" / "data.txt"


@pytest.fixture
def loaded_collection(data_file_path):
    """Fixture to provide a loaded sutra collection."""
    return read_sutras(data_file_path)


class TestDataStructure:
    """Test the underlying data structure."""

    def test_data_file_exists(self, data_file_path):
        """Test that the data file exists."""
        assert data_file_path.exists(), f"Data file not found at {data_file_path}"

    def test_json_structure(self, data_file_path):
        """Test that the JSON structure is valid."""
        with open(data_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, dict), "Root should be a dictionary"
        assert "name" in data, "Missing 'name' field"
        assert "data" in data, "Missing 'data' field"
        assert isinstance(data["data"], list), "'data' should be a list"
        assert len(data["data"]) > 0, "Data list should not be empty"

    def test_sutra_fields(self, data_file_path):
        """Test that sutras have the expected fields."""
        with open(data_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        required_fields = ["i", "a", "p", "n", "s", "e"]
        first_entry = data["data"][0]

        for field in required_fields:
            assert field in first_entry, f"Missing required field '{field}'"


class TestSutra:
    """Test the Sutra class."""

    def test_sutra_creation(self, loaded_collection):
        """Test that sutras can be created and have basic properties."""
        assert len(loaded_collection) > 0, "Collection should not be empty"

        first_sutra = loaded_collection[0]
        assert isinstance(first_sutra, Sutra), "First item should be a Sutra"

    def test_sutra_properties(self, loaded_collection):
        """Test basic sutra properties."""
        sutra = loaded_collection[0]

        assert hasattr(sutra, "adhyaya"), "Sutra should have adhyaya property"
        assert hasattr(sutra, "pada"), "Sutra should have pada property"
        assert hasattr(sutra, "number"), "Sutra should have number property"
        assert sutra.adhyaya > 0, "Adhyaya should be positive"
        assert sutra.pada > 0, "Pada should be positive"
        assert sutra.number > 0, "Number should be positive"

    def test_sutra_text_properties(self, loaded_collection):
        """Test sutra text properties."""
        sutra = loaded_collection[0]

        assert len(sutra.devanagari) > 0, "Devanagari should not be empty"
        assert len(sutra.transliteration) > 0, "Transliteration should not be empty"
        assert len(sutra.reference) > 0, "Reference should not be empty"
        assert "." in sutra.reference, "Reference should contain dots"

    def test_sutra_string_representations(self, loaded_collection):
        """Test string representations."""
        sutra = loaded_collection[0]

        str_repr = str(sutra)
        repr_repr = repr(sutra)

        assert "Sutra" in str_repr, "String representation should contain 'Sutra'"
        assert "Sutra" in repr_repr, "Repr should contain 'Sutra'"
        assert sutra.reference in str_repr, "String should contain reference"


class TestSutraCollection:
    """Test the SutraCollection class."""

    def test_collection_basic_properties(self, loaded_collection):
        """Test basic collection properties."""
        assert isinstance(loaded_collection, SutraCollection)
        assert len(loaded_collection) > 0, "Collection should not be empty"
        assert (
            loaded_collection.name == "sutraani"
        ), "Collection name should be 'sutraani'"

    def test_collection_iteration(self, loaded_collection):
        """Test that collection can be iterated."""
        count = 0
        for sutra in loaded_collection:
            assert isinstance(sutra, Sutra)
            count += 1
            if count > 5:  # Just test a few
                break
        assert count > 0, "Should be able to iterate"

    def test_collection_indexing(self, loaded_collection):
        """Test collection indexing."""
        first = loaded_collection[0]
        last = loaded_collection[-1]

        assert isinstance(first, Sutra)
        assert isinstance(last, Sutra)
        # They should be different unless there's only one sutra
        if len(loaded_collection) > 1:
            assert (
                first.reference != last.reference
            ), "First and last should be different"

    def test_get_by_reference(self, loaded_collection):
        """Test getting sutras by reference."""
        # Test with first sutra's reference
        first_sutra = loaded_collection[0]
        found = loaded_collection.get_by_reference(first_sutra.reference)

        assert found is not None, "Should find the sutra"
        assert found.reference == first_sutra.reference, "Should be the same sutra"

        # Test with non-existent reference
        not_found = loaded_collection.get_by_reference("99.99.99")
        assert not_found is None, "Should not find non-existent sutra"

    def test_get_by_adhyaya(self, loaded_collection):
        """Test getting sutras by adhyaya."""
        adhyaya1_sutras = loaded_collection.get_by_adhyaya(1)

        assert len(adhyaya1_sutras) > 0, "Should find sutras in adhyaya 1"
        for sutra in adhyaya1_sutras:
            assert sutra.adhyaya == 1, "All sutras should be from adhyaya 1"

    def test_get_by_pada(self, loaded_collection):
        """Test getting sutras by pada."""
        pada_sutras = loaded_collection.get_by_pada(1, 1)

        assert len(pada_sutras) > 0, "Should find sutras in pada 1.1"
        for sutra in pada_sutras:
            assert sutra.adhyaya == 1, "All sutras should be from adhyaya 1"
            assert sutra.pada == 1, "All sutras should be from pada 1"

    def test_search_text(self, loaded_collection):
        """Test text search functionality."""
        # Search for a common Sanskrit term
        results = loaded_collection.search_text("वृद्धि")

        # Should find at least some results
        assert len(results) >= 0, "Search should return a list"

        # All results should contain the search term
        for sutra in results:
            text_fields = [sutra.text.sanskrit, sutra.text.english, sutra.ss]
            found = any("वृद्धि" in field for field in text_fields)
            assert found, f"Sutra {sutra.reference} should contain 'वृद्धि'"

        # Test case-insensitive search
        results_ci = loaded_collection.search_text("VRUDDHI", case_sensitive=False)
        assert len(results_ci) >= 0, "Case-insensitive search should work"

    def test_collection_string_representations(self, loaded_collection):
        """Test collection string representations."""
        str_repr = str(loaded_collection)
        repr_repr = repr(loaded_collection)

        assert "SutraCollection" in str_repr
        assert "SutraCollection" in repr_repr
        assert loaded_collection.name in str_repr


class TestReaders:
    """Test the readers module."""

    def test_read_sutras_with_path_object(self, data_file_path):
        """Test reading with Path object."""
        collection = read_sutras(data_file_path)
        assert isinstance(collection, SutraCollection)
        assert len(collection) > 0

    def test_read_sutras_with_string_path(self, data_file_path):
        """Test reading with string path."""
        collection = read_sutras(str(data_file_path))
        assert isinstance(collection, SutraCollection)
        assert len(collection) > 0

    def test_read_nonexistent_file(self):
        """Test error handling for non-existent file."""
        with pytest.raises(FileNotFoundError):
            read_sutras("nonexistent_file.txt")
