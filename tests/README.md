# Tests for Vyakarana Package

This directory contains comprehensive tests for the Vyakarana Sanskrit Grammar package.

## Test Files

- `test_sutras.py` - Main test suite that can be run standalone
- `test_vyakarana_pytest.py` - Pytest-compatible test suite
- `conftest.py` - Pytest configuration and fixtures
- `run_tests.py` - Simple test runner script

## Running Tests

### Option 1: Standalone Test Runner

Run the tests without any external dependencies:

```bash
cd tests
python3 test_sutras.py
```

Or use the test runner:

```bash
cd tests
python3 run_tests.py
```

### Option 2: Using Pytest

First install pytest:

```bash
pip install pytest
# or
pip install -e .[test]
```

Then run the tests:

```bash
# From the root directory
pytest tests/

# From the tests directory
cd tests
pytest test_vyakarana_pytest.py
```

### Option 3: From Root Directory

```bash
# Run standalone tests
python3 tests/test_sutras.py

# Run with pytest (if installed)
pytest tests/
```

## Test Coverage

The tests cover:

- **Data Structure Validation**: Ensures the JSON data format is correct
- **Sutra Class**: Tests all properties and methods of individual sutras
- **SutraCollection Class**: Tests collection operations, filtering, and search
- **Readers Module**: Tests file reading and parsing functionality
- **Error Handling**: Tests proper error handling for invalid inputs

## Expected Output

A successful test run should show:

```
✅ JSON structure valid
✅ Successfully read XXXX sutras
✅ First sutra: 1.1.1 - वृद्धिरादैच्
✅ Search found XX sutras containing 'वृद्धि'
✅ Found sutra 1.1.1: वृद्धिरादैच्
✅ Found XX sutras in Adhyaya 1, Pada 1
🎉 All tests passed!
```

## Adding New Tests

To add new tests:

1. For standalone tests: Add functions to `test_sutras.py`
2. For pytest: Add test methods to classes in `test_vyakarana_pytest.py`
3. Follow the existing naming conventions and patterns
