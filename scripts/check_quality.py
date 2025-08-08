#!/usr/bin/env python3
"""
Local development script to run all quality checks that GitHub Actions will run.

This script helps you verify that your code will pass CI/CD checks before pushing.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and report the result."""
    print(f"\n🔍 {description}")
    print("=" * 50)

    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} - PASSED")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def main():
    """Run all quality checks."""
    print("🚀 Running local quality checks...")
    print("This simulates what GitHub Actions will run.")

    checks = [
        ("python -m pytest tests/ -v", "Running tests"),
        ("black --check --diff vyakarana/ tests/", "Code formatting (black)"),
        ("isort --check-only --diff vyakarana/ tests/", "Import sorting (isort)"),
        (
            "flake8 vyakarana/ tests/ --count --select=E9,F63,F7,F82",
            "Critical linting (flake8)",
        ),
        (
            "mypy vyakarana/ --ignore-missing-imports --no-strict-optional",
            "Type checking (mypy)",
        ),
        ("coverage run -m pytest tests/ && coverage report", "Coverage analysis"),
    ]

    results = []
    for cmd, description in checks:
        success = run_command(cmd, description)
        results.append((description, success))

    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)

    all_passed = True
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:8} {description}")
        if not success:
            all_passed = False

    if all_passed:
        print("\n🎉 All checks passed! Your code is ready for CI/CD.")
        sys.exit(0)
    else:
        print("\n⚠️  Some checks failed. Please fix the issues before pushing.")
        sys.exit(1)


if __name__ == "__main__":
    # Check if we're in the right directory
    if not Path("vyakarana").exists():
        print("❌ Error: Please run this script from the project root directory.")
        sys.exit(1)

    main()
