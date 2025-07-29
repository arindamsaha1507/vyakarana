# Changelog

All notable changes to the Vyakarana package will be documented in this file.

## [0.1.0] - 2025-07-29

### Added

- Initial release of the Vyakarana Python package
- `Sutra` dataclass for representing individual Sanskrit grammar sutras
- `SutraCollection` class for managing collections of sutras
- `read_sutras()` function for parsing JSON data files
- Comprehensive search and filtering capabilities
- Support for reference-based lookups (e.g., "1.1.1")
- Text search functionality with case-sensitive/insensitive options
- Filtering by adhyaya (chapter) and pada (quarter)
- Rich string representations and properties
- Comprehensive test suite in `tests/` directory
- Both standalone and pytest-compatible tests
- Example usage scripts
- Full package structure with setup.py

### Features

- Read and parse Ashtadhyayi sutra data from JSON format
- Type-safe dataclasses with proper validation
- Intuitive API for working with Sanskrit grammatical data
- Search sutras by text content
- Filter sutras by structural properties
- Proper error handling and informative error messages

### Data Support

- Complete Ashtadhyayi sutra collection (3983+ sutras)
- Sanskrit text in Devanagari script
- English transliterations
- Traditional commentary classifications
- Metadata and contextual information
