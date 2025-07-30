#!/usr/bin/env python3
"""
Simple test runner for the Vyakarana package.

This script runs tests without requiring pytest installation.
"""

import subprocess
import sys
from pathlib import Path


if __name__ == "__main__":
    print("Running Vyakarana test suite...")
    print("=" * 50)

    # Get the test file path
    test_file = Path(__file__).parent / "test_sutras.py"

    # Check if the test file exists
    if not test_file.exists():
        print(f"Error: Test file not found: {test_file}")
        sys.exit(1)

    try:
        # Run the test file as a subprocess
        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,  # Don't raise exception on non-zero exit code
        )

        # Print the output
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)

        # Exit with the same code as the test
        sys.exit(result.returncode)

    except (subprocess.SubprocessError, OSError) as e:
        print(f"Error running tests: {e}")
        sys.exit(1)
