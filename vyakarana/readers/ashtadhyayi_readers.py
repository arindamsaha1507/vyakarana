"""
Data readers for Ashtadhyayi Sanskrit Grammar data files.

This module provides functions to read and parse Ashtadhyayi sutras data
files into structured objects.
"""

import json
from pathlib import Path
from typing import Union, Dict, Any

from vyakarana.models import (
    Sutra,
    SutraCollection,
    SutraIdentifier,
    SutraText,
    SutraReferences,
    PadaVibhaga,
    SutraTypeInfo,
    Backlinks,
)


def read_sutras(file_path: Union[str, Path]) -> SutraCollection:
    """
    Read and parse a sutras data file into a SutraCollection.

    The file should be in JSON format with the structure:
    {
        "name": "collection_name",
        "data": [
            {
                "i": "11001",
                "a": "1",
                "p": "1",
                "n": "1",
                "s": "वृद्धिरादैच्",
                ...
            },
            ...
        ]
    }

    Args:
        file_path: Path to the sutras data file

    Returns:
        SutraCollection object containing all the sutras

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file is not valid JSON
        KeyError: If required fields are missing from the data
        ValueError: If the data structure is invalid
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Sutras data file not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file {file_path}: {e}") from e

    # Validate the basic structure
    if not isinstance(data, dict):
        raise ValueError(f"Expected dict at root level, got {type(data)}")

    if "name" not in data:
        raise KeyError("Missing 'name' field in data")

    if "data" not in data:
        raise KeyError("Missing 'data' field in data")

    if not isinstance(data["data"], list):
        raise ValueError(f"Expected list for 'data' field, got {type(data['data'])}")

    # Parse each sutra entry
    sutras = []
    required_fields = [
        "i",
        "a",
        "p",
        "n",
        "s",
        "e",
        "skn",
        "lskn",
        "mskn",
        "sskn",
        "plskn",
        "lpn",
        "pc",
        "sk_chapter",
        "lsk_chapter",
        "type",
        "an",
        "ad",
        "ss",
    ]

    for i, sutra_data in enumerate(data["data"]):
        if not isinstance(sutra_data, dict):
            raise ValueError(
                f"Expected dict for sutra at index {i}, got {type(sutra_data)}"
            )

        # Check for required fields
        missing_fields = [field for field in required_fields if field not in sutra_data]
        if missing_fields:
            raise KeyError(
                f"Missing required fields in sutra at index {i}: {missing_fields}"
            )

        # Create Sutra object
        try:
            # Convert string values to appropriate types
            adhyaya = int(sutra_data["a"])
            pada = int(sutra_data["p"])
            number = int(sutra_data["n"])

            # Create identifier object
            identifier = SutraIdentifier(adhyaya=adhyaya, pada=pada, number=number)

            # Create text object
            text = SutraText(
                sanskrit=str(sutra_data["s"]), english=str(sutra_data["e"])
            )

            # Create references object - convert to int, default to 0 for empty/invalid values
            def safe_int(value, default=0):
                try:
                    return int(value) if value and str(value).strip() else default
                except (ValueError, TypeError):
                    return default

            references = SutraReferences(
                skn=safe_int(sutra_data["skn"]),
                lskn=safe_int(sutra_data["lskn"]),
                mskn=safe_int(sutra_data["mskn"]),
                sskn=safe_int(sutra_data["sskn"]),
                plskn=safe_int(sutra_data["plskn"]),
                lpn=safe_int(sutra_data["lpn"]),
                sk_chapter=safe_int(sutra_data["sk_chapter"]),
                lsk_chapter=safe_int(sutra_data["lsk_chapter"]),
            )

            # Parse pada vibhaga (grammatical analysis)
            pada_vibhaga = None
            if sutra_data["pc"]:
                try:
                    pada_vibhaga = PadaVibhaga.from_string(str(sutra_data["pc"]))
                except (ValueError, IndexError):
                    # If parsing fails, keep it as None
                    pada_vibhaga = None

            # Parse sutra type information
            sutra_type_info = SutraTypeInfo.from_string(str(sutra_data["type"]))

            # Parse backlinks (anuvritti and adhikara)
            backlinks = Backlinks.from_strings(
                str(sutra_data["an"]), str(sutra_data["ad"])
            )

            sutra = Sutra(
                identifier=identifier,
                text=text,
                references=references,
                pada_vibhaga=pada_vibhaga,
                sutra_type_info=sutra_type_info,
                backlinks=backlinks,
                ss=str(sutra_data["ss"]),
            )
            sutras.append(sutra)
        except Exception as e:
            raise ValueError(f"Error creating Sutra object at index {i}: {e}") from e

    return SutraCollection(name=data["name"], sutras=sutras)


def _validate_sutra_data(sutra_data: Dict[str, Any], index: int) -> None:
    """
    Validate a single sutra data dictionary.

    Args:
        sutra_data: Dictionary containing sutra data
        index: Index of the sutra for error reporting

    Raises:
        ValueError: If validation fails
    """
    # Additional validation can be added here
    # For example, checking if 'a', 'p', 'n' are numeric strings
    try:
        int(sutra_data["a"])  # adhyaya should be numeric
        int(sutra_data["p"])  # pada should be numeric
        int(sutra_data["n"])  # number should be numeric
    except (ValueError, TypeError) as exc:
        raise ValueError(f"Sutra at index {index} has invalid numeric fields") from exc


def get_data_file_path(filename: str) -> Path:
    """
    Get the path to a data file in the package.

    Args:
        filename: Name of the data file

    Returns:
        Path object pointing to the data file
    """
    # This assumes the data files are in the same directory as this module
    # or in a 'data' subdirectory
    current_dir = Path(__file__).parent

    # Try current directory first
    file_path = current_dir / filename
    if file_path.exists():
        return file_path

    # Try parent directory (where the original files are)
    file_path = current_dir.parent / filename
    if file_path.exists():
        return file_path

    # Try going up two levels (readers/vyakarana/filename)
    file_path = current_dir.parent.parent / filename
    if file_path.exists():
        return file_path

    # Try specific subdirectories
    for subdir in ["sutraani", "data"]:
        file_path = current_dir.parent.parent / subdir / filename
        if file_path.exists():
            return file_path

    raise FileNotFoundError(f"Data file '{filename}' not found in expected locations")


def read_sutras_from_package() -> SutraCollection:
    """
    Read the sutras data file that comes with the package.

    Returns:
        SutraCollection object containing all the sutras
    """
    file_path = get_data_file_path("sutraani/data.txt")
    return read_sutras(file_path)
