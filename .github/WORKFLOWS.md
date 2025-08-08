# GitHub Actions Setup for Vyakarana

This repository now includes comprehensive GitHub Actions workflows for continuous integration and code quality.

## Workflows

### 1. Tests and Coverage (`.github/workflows/test.yml`)

- **Triggers**: Push to master/main/develop, pull requests, manual dispatch
- **Python versions**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Features**:
  - Runs full test suite with pytest
  - Generates coverage reports
  - Uploads coverage to Codecov (when configured)
  - Tests package installation
  - Caches pip dependencies for faster builds

### 2. Code Quality (`.github/workflows/quality.yml`)

- **Triggers**: Push to master/main/develop, pull requests
- **Features**:
  - Code formatting check with Black
  - Import sorting check with isort
  - Linting with flake8
  - Security scanning with Bandit
  - Uploads security reports as artifacts

### 3. Security Checks (`.github/workflows/security.yml`)

- **Triggers**: Weekly schedule (Sundays 3 AM UTC), manual dispatch
- **Features**:
  - Dependency vulnerability scanning with pip-audit
  - Security analysis with Safety
  - Uploads security reports as artifacts

## Configuration Files

### `pyproject.toml`

Contains configuration for:

- **Coverage**: Source paths, exclusions, reporting thresholds
- **Black**: Code formatting rules
- **isort**: Import sorting preferences
- **mypy**: Type checking settings

### `setup.py` (Updated)

- Added Python 3.12 support
- Enhanced development dependencies
- Added security tools group

## Local Development Tools

### Quality Check Script (`scripts/check_quality.py`)

Run locally to simulate CI/CD checks:

```bash
python scripts/check_quality.py
```

### Enhanced Makefile

New targets:

- `make test-coverage`: Run tests with coverage
- `make quality`: Run local quality checks
- `make ci-check`: Simulate CI checks exactly
- `make clean`: Clean all artifacts including coverage files

## Usage

### Running Tests Locally

```bash
# Basic test run
make test-pytest

# With coverage
make test-coverage

# Full quality check (like CI)
make ci-check
```

### Before Committing

```bash
# Format code
make format

# Check everything
make quality
```

## Badges for README

Add these badges to your README.md:

```markdown
![Tests](https://github.com/arindamsaha1507/vyakarana/workflows/Tests%20and%20Coverage/badge.svg)
![Code Quality](https://github.com/arindamsaha1507/vyakarana/workflows/Code%20Quality/badge.svg)
[![codecov](https://codecov.io/gh/arindamsaha1507/vyakarana/branch/master/graph/badge.svg)](https://codecov.io/gh/arindamsaha1507/vyakarana)
```

## Setup Instructions

1. **Push to GitHub**: The workflows will activate automatically
2. **Codecov (Optional)**:
   - Visit https://codecov.io/
   - Connect your GitHub repository
   - Coverage reports will be uploaded automatically
3. **Branch Protection**: Consider enabling branch protection rules that require CI checks to pass

## Workflow Features

- **Dependency Caching**: Speeds up builds
- **Matrix Testing**: Tests across multiple Python versions
- **Artifact Upload**: Saves reports for review
- **Security Scanning**: Regular vulnerability checks
- **Automated Formatting Checks**: Ensures code consistency

The setup provides professional-grade CI/CD with comprehensive testing, quality checks, and security monitoring.
