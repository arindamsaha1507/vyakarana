# Vyakarana: Sanskrit Grammar Python Package

A Python package for working with Sanskrit grammatical data, particularly Panini's Ashtadhyayi sutras and related linguistic resources.

**Note**: This repository contains the entire data that powers https://ashtadhyayi.com. The website reads all the data directly from this repository.

## Features

- **Sutra Management**: Read, parse, and organize Sanskrit grammar sutras
- **Rich Data Models**: Type-safe dataclasses for representing grammatical concepts
- **Search & Filter**: Find sutras by text content, reference, or structural properties
- **Extensible**: Designed to accommodate additional grammatical resources

## Installation

### From Source

```bash
git clone https://github.com/arindamsaha1507/vyakarana.git
cd vyakarana
pip install -e .
```

### Dependencies

- Python 3.8+
- pydantic >= 2.0.0

## Quick Start

```python
from vyakarana import read_sutras

# Read sutras from the data file
collection = read_sutras("sutraani/data.txt")

print(f"Loaded {len(collection)} sutras")

# Get a specific sutra
sutra = collection.get_by_reference("1.1.1")
print(f"Sutra 1.1.1: {sutra.devanagari}")

# Search for sutras
results = collection.search_text("वृद्धि")
print(f"Found {len(results)} sutras containing 'वृद्धि'")

# Get sutras from a specific chapter
chapter1_sutras = collection.get_by_adhyaya(1)
print(f"Adhyaya 1 has {len(chapter1_sutras)} sutras")
```

## Data Structure

Each sutra contains the following information:

- **Reference**: Adhyaya, Pada, and Sutra number (e.g., "1.1.1")
- **Text**: Sanskrit text in Devanagari script
- **Transliteration**: Roman transliteration
- **Classifications**: Various traditional commentary classifications
- **Metadata**: Additional linguistic and contextual information

## API Reference

### Sutra Class

```python
@dataclass
class Sutra:
    i: str              # Unique identifier
    a: str              # Adhyaya (chapter)
    p: str              # Pada (quarter)
    n: str              # Sutra number
    s: str              # Sanskrit text
    e: str              # English transliteration
    # ... additional fields

    @property
    def reference(self) -> str:
        """Returns formatted reference like '1.1.1'"""

    @property
    def devanagari(self) -> str:
        """Returns Sanskrit text"""

    @property
    def transliteration(self) -> str:
        """Returns English transliteration"""
```

### SutraCollection Class

```python
class SutraCollection:
    def __len__(self) -> int:
        """Number of sutras"""

    def get_by_reference(self, reference: str) -> Optional[Sutra]:
        """Get sutra by reference (e.g., '1.1.1')"""

    def get_by_adhyaya(self, adhyaya: int) -> List[Sutra]:
        """Get all sutras from a chapter"""

    def get_by_pada(self, adhyaya: int, pada: int) -> List[Sutra]:
        """Get all sutras from a specific pada"""

    def search_text(self, text: str, case_sensitive: bool = False) -> List[Sutra]:
        """Search sutras by text content"""
```

## Data Format

The package expects data in JSON format:

```json
{
  "name": "sutraani",
  "data": [
    {
      "i": "11001",
      "a": "1",
      "p": "1",
      "n": "1",
      "s": "वृद्धिरादैच्",
      "e": "vruddhiraadaich",
      "skn": "16",
      "lskn": "32",
      "pc": "वृद्धिः$S$1$1$##आत्-ऐच्$S$1$1$",
      "type": "S$वृद्धिसंज्ञा$",
      "ss": "आत्-ऐच् वृद्धिः",
      "rpn": "1"
    }
  ]
}
```

## Testing

The package includes comprehensive tests in the `tests/` directory.

### Run Tests (Simple)

```bash
# From root directory
python3 tests/test_sutras.py

# From tests directory  
cd tests
python3 test_sutras.py
```

### Run Tests (with pytest)

```bash
# Install test dependencies
pip install -e .[test]

# Run pytest
pytest tests/
```

See `tests/README.md` for detailed testing information.

## Repository Structure

This repository contains extensive Sanskrit grammatical data:

- `sutraani/` - Panini's Ashtadhyayi sutras
- `dhatu/` - Verbal root forms and conjugations
- `kosha/` - Various Sanskrit dictionaries
- `shabda/` - Word forms and declensions
- `vyakarana/` - Python package for data access

## Data Editing Guidelines

**Direct edits to this repository are discouraged for sutrapatha commentaries, dhatu forms and shabda forms.** Please use the "edit" button available on the website (https://ashtadhyayi.com) to make changes wherever possible.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License.

## Acknowledgments

This package is built around the rich tradition of Sanskrit grammatical analysis, particularly:

- Panini's Ashtadhyayi
- Traditional commentaries and classifications
- Modern computational linguistic approaches to Sanskrit

## Contact

For questions or support, please open an issue on GitHub.
