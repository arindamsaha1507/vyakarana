#!/usr/bin/env python3
"""
Test suite for the Vyakarana package.

This module contains comprehensive tests for reading and parsing sutra data.
"""

import json
import sys
from pathlib import Path

# Add the parent directory to the path to import vyakarana
sys.path.insert(0, str(Path(__file__).parent.parent))

from vyakarana import read_sutras


def test_basic_functionality():
    """Test basic reading and parsing functionality."""
    print("Testing Vyakarana package functionality...")

    # Get the data file path (go up from tests/ to root, then to sutraani/)
    current_dir = Path(__file__).parent
    data_file = current_dir.parent / "sutraani" / "data.txt"

    if not data_file.exists():
        print(f"❌ Data file not found at {data_file}")
        raise FileNotFoundError(f"Data file not found at {data_file}")

    try:
        # Read the sutras
        collection = read_sutras(data_file)
        print(f"✅ Successfully read {len(collection)} sutras")

        # Test basic properties
        if len(collection) == 0:
            print("❌ No sutras found in collection")
            raise AssertionError("No sutras found in collection")

        # Test first sutra
        first_sutra = collection[0]
        print(f"✅ First sutra: {first_sutra.reference} - {first_sutra.devanagari}")

        # Test search functionality
        search_results = collection.search_text("वृद्धि")
        print(f"✅ Search found {len(search_results)} sutras containing 'वृद्धि'")

        # Test reference lookup
        sutra_111 = collection.get_by_reference("1.1.1")
        if sutra_111:
            print(f"✅ Found sutra 1.1.1: {sutra_111.devanagari}")
        else:
            print("⚠️  Sutra 1.1.1 not found")

        # Test chapter/pada filtering
        pada_sutras = collection.get_by_pada(1, 1)
        print(f"✅ Found {len(pada_sutras)} sutras in Adhyaya 1, Pada 1")

        print("🎉 All tests passed!")

    except (ValueError, FileNotFoundError, KeyError) as e:
        print(f"❌ Error during testing: {e}")
        raise AssertionError(f"Basic functionality test failed: {e}") from e


def test_data_structure():
    """Test the underlying data structure."""
    print("\nTesting data structure...")

    current_dir = Path(__file__).parent
    data_file = current_dir.parent / "sutraani" / "data.txt"

    try:
        # Read raw JSON to verify structure
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        print("✅ JSON structure valid")
        print(f"✅ Collection name: {data['name']}")
        print(f"✅ Number of entries: {len(data['data'])}")

        # Check first entry structure
        if data["data"]:
            first_entry = data["data"][0]
            required_fields = ["i", "a", "p", "n", "s", "e"]
            for field in required_fields:
                if field in first_entry:
                    print(f"✅ Field '{field}' present")
                else:
                    print(f"❌ Field '{field}' missing")
                    raise AssertionError(f"Required field '{field}' missing from data structure")

    except (ValueError, FileNotFoundError, KeyError, TypeError) as e:
        print(f"❌ Data structure test failed: {e}")
        raise AssertionError(f"Data structure test failed: {e}") from e


def test_sutra_properties():
    """Test individual sutra properties and methods."""
    print("\nTesting sutra properties...")

    current_dir = Path(__file__).parent
    data_file = current_dir.parent / "sutraani" / "data.txt"

    try:
        collection = read_sutras(data_file)

        if len(collection) == 0:
            print("❌ No sutras to test")
            raise AssertionError("No sutras to test")

        # Test first sutra properties
        sutra = collection[0]

        # Test numeric properties
        assert isinstance(sutra.adhyaya, int), "Adhyaya should be int"
        assert isinstance(sutra.pada, int), "Pada should be int"
        assert isinstance(sutra.number, int), "Number should be int"
        print("✅ Numeric properties work correctly")

        # Test string properties
        assert len(sutra.reference) > 0, "Reference should not be empty"
        assert len(sutra.devanagari) > 0, "Devanagari should not be empty"
        assert len(sutra.transliteration) > 0, "Transliteration should not be empty"
        print("✅ String properties work correctly")

        # Test string representations
        str_repr = str(sutra)
        repr_repr = repr(sutra)
        assert "Sutra" in str_repr, "String representation should contain 'Sutra'"
        assert "Sutra" in repr_repr, "Repr should contain 'Sutra'"
        print("✅ String representations work correctly")

    except (ValueError, AttributeError, TypeError) as e:
        print(f"❌ Sutra properties test failed: {e}")
        raise AssertionError(f"Sutra properties test failed: {e}") from e


def test_collection_methods():
    """Test SutraCollection methods."""
    print("\nTesting collection methods...")

    current_dir = Path(__file__).parent
    data_file = current_dir.parent / "sutraani" / "data.txt"

    try:
        collection = read_sutras(data_file)

        # Test iteration
        count = 0
        for _ in collection:
            count += 1
            if count > 5:  # Just test a few
                break
        print(f"✅ Iteration works - tested {count} sutras")

        # Test indexing
        first = collection[0]
        last = collection[-1]
        assert first != last, "First and last sutras should be different"
        print("✅ Indexing works correctly")

        # Test length
        length = len(collection)
        assert length > 0, "Collection should not be empty"
        print(f"✅ Length method works - {length} sutras")

        # Test filtering methods
        adhyaya1 = collection.get_by_adhyaya(1)
        assert len(adhyaya1) > 0, "Should find sutras in adhyaya 1"
        print(f"✅ Adhyaya filtering works - found {len(adhyaya1)} sutras")

        pada11 = collection.get_by_pada(1, 1)
        assert len(pada11) > 0, "Should find sutras in pada 1.1"
        print(f"✅ Pada filtering works - found {len(pada11)} sutras")

        # Test string representation
        collection_str = str(collection)
        assert (
            "SutraCollection" in collection_str
        ), "String should contain 'SutraCollection'"
        print("✅ Collection string representation works")

    except (ValueError, FileNotFoundError, AttributeError, TypeError) as e:
        print(f"❌ Collection methods test failed: {e}")
        raise AssertionError(f"Collection methods test failed: {e}") from e


if __name__ == "__main__":
    print("Vyakarana Package Test Suite")
    print("=" * 50)

    tests = [
        test_data_structure,
        test_basic_functionality,
        test_sutra_properties,
        test_collection_methods,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            print(f"✅ {test_func.__name__} passed")
            passed += 1
        except (ValueError, FileNotFoundError, AttributeError, TypeError, AssertionError) as e:
            print(f"❌ Test {test_func.__name__} failed with exception: {e}")
            failed += 1

    print("\n📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Total: {passed + failed}")

    if failed == 0:
        print("\n🎉 All tests completed successfully!")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the output above.")
