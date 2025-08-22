# CI/CD Version Bumping Toolkit

A Python-based automation toolkit for semantic version bumping in CI/CD pipelines. This project provides utilities to automatically extract bump types from commit messages and update version numbers across different project types.

## Features

- **Automatic Bump Type Detection**: Extract version bump types (`major`, `minor`, `patch`) from commit messages
- **Multi-Project Support**: Works with generic VERSION files and extensible to other project types
- **GitHub Actions Integration**: Ready-to-use workflow templates for automated version bumping
- **Semantic Versioning**: Full support for semantic versioning with optional build numbers

## Project Structure

```
ci-cd/
├── workflows/
│   ├── extract_bump_type.py      # Extract bump type from commit messages
│   ├── generic_bump_version.py   # Generic version bumping for VERSION files
│   └── flutter/                  # Flutter/Dart specific implementations
│       ├── flutter_bump_version.py  # Flutter version bumping
│       ├── bump_version.yaml        # GitHub Actions workflow template
│       └── README.md                # Flutter-specific documentation
├── tests/                         # Test suite
├── pyproject.toml                # Python project configuration
├── VERSION                       # Current project version
└── README.md                     # This file
```

## Usage

### Commit Message Format

#### First, be sure GitHub Actions have write permissions to your repository.
- Go to Settings > Actions > Workflow permissions > Read and write permissions

and save!

To trigger automatic version bumping, include a `Bump:` directive at the end of your commit message:

```
fix(auth): resolve login issue Bump:patch
feat(api): add new endpoint Bump:minor
feat!: breaking change in API Bump:major
```

**Supported bump types:**
- `major`: Breaking changes (x.0.0)
- `minor`: New features (0.x.0)
- `patch`: Bug fixes (0.0.x)

If no `Bump:` directive is found, it defaults to `patch`.

### Extract Bump Type

```bash
python3 workflows/extract_bump_type.py "fix(test): random message Bump:patch"
# Output: patch
```

### Generic Version Bumping

For projects using a simple `VERSION` file:

```bash
python3 workflows/generic_bump_version.py patch
```

Supports version formats:
- `1.0.0` (semantic versioning)
- `1.0.0+1` (with build number)

### Project-Specific Implementations

Different project types may have specific version bumping requirements:

- **Flutter/Dart Projects**: See `workflows/flutter/README.md` for pubspec.yaml handling
- **Generic Projects**: Use the standard VERSION file approach above
- **Custom Projects**: Extend the base classes for your specific needs

## GitHub Actions Integration

### Generic Projects

The scripts can be easily integrated into any CI/CD pipeline:

```yaml
- name: Bump Version
  run: |
    COMMIT_MSG=$(git log -1 --pretty=%B)
    BUMP_TYPE=$(python3 extract_bump_type.py "$COMMIT_MSG")
    python3 generic_bump_version.py $BUMP_TYPE
```

### Project-Specific Workflows

For specific project types with dedicated workflows:

- **Flutter Projects**: See `workflows/flutter/README.md` for complete GitHub Actions setup
- **Other Projects**: Adapt the generic example above for your specific version file format

## Installation

### Requirements

- Python 3.12+
- Poetry (for development)

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd ci-cd

# Install dependencies (development)
poetry install
```

## Error Handling

The toolkit includes robust error handling:

- **Invalid bump types**: Returns `error` for unsupported bump types
- **Malformed commit messages**: Gracefully handles parsing errors
- **File access issues**: Clear error messages for missing files
- **Version format validation**: Ensures semantic versioning compliance

## Examples

### Example 1: Patch Bump

```bash
# Current version: 1.2.3
python3 workflows/generic_bump_version.py patch
# New version: 1.2.4
```

### Example 2: Minor Bump with Build Number

```bash
# Current version: 1.2.3+5
python3 workflows/generic_bump_version.py minor
# New version: 1.3.0+6
```

### Example 3: Project-Specific Usage

```bash
# For Flutter projects (see workflows/flutter/README.md)
python3 workflows/flutter/flutter_bump_version.py major

# For generic VERSION file projects
python3 workflows/generic_bump_version.py patch
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes and add tests
4. Run the test suite: `poetry run pytest`
5. Commit your changes: `git commit -m "feat: add new feature Bump:minor"`
6. Push to the branch: `git push origin feature/new-feature`
7. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*This toolkit is designed to streamline version management in CI/CD pipelines, making semantic versioning automation simple and reliable.*
