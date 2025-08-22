# Flutter/Dart Version Bumping

Automated semantic version bumping specifically designed for Flutter and Dart projects using `pubspec.yaml` files.

## Overview

This module provides specialized version management for Flutter and Dart projects by directly updating the `version` field in `pubspec.yaml` files. It supports both semantic versioning and build numbers commonly used in Flutter applications.

## Features

- **pubspec.yaml Integration**: Direct manipulation of Flutter/Dart project version files
- **Build Number Support**: Handles Flutter build numbers (e.g., `1.0.0+1`)
- **Semantic Versioning**: Full support for major.minor.patch versioning
- **GitHub Actions Ready**: Pre-configured workflow for automated version bumping

## Usage

### Command Line Interface

```bash
# Bump patch version (1.0.0 → 1.0.1)
python3 flutter_bump_version.py patch

# Bump minor version (1.0.0 → 1.1.0)
python3 flutter_bump_version.py minor

# Bump major version (1.0.0 → 2.0.0)
python3 flutter_bump_version.py major

# Bump build number only (1.0.0+1 → 1.0.0+2)
python3 flutter_bump_version.py build
```

### Supported Version Formats

The Flutter version bumper supports various `pubspec.yaml` version formats:

```yaml
# Simple semantic versioning
version: 1.0.0

# With build number (recommended for Flutter apps)
version: 1.0.0+1
```

## GitHub Actions Integration

### Setup

1. Copy the workflow template to your Flutter project:
   ```bash
   cp bump_version.yaml .github/workflows/
   ```

2. Ensure the workflow scripts are accessible in your project root or update paths accordingly.

### Workflow Configuration

The included `bump_version.yaml` provides a complete GitHub Actions workflow:

```yaml
name: Bump Version

on:
  push:
    branches:
      - main

jobs:
  bump-version:
    runs-on: ubuntu-latest
    steps:
      - name: Git setup
        uses: actions/checkout@v4
      
      - name: Decide bump type
        id: decide_bump
        run: |
          COMMIT_MSG=$(git log -1 --pretty=%B)
          BUMP_TYPE=$(python3 extract_bump_type.py "$COMMIT_MSG")
          echo "bump_type=$BUMP_TYPE" >> $GITHUB_OUTPUT
          
      - name: Bump version
        run: python3 flutter_bump_version.py ${{ steps.decide_bump.outputs.bump_type }}
        
      - name: Commit changes
        run: |
          git add pubspec.yaml
          git commit -m "chore: bump version [skip ci]"
          git push
```

### Workflow Features

- **Automatic Trigger**: Runs on every push to the main branch
- **Commit Message Parsing**: Extracts bump type from commit messages
- **Error Handling**: Fails gracefully on invalid bump types
- **Skip CI**: Prevents recursive workflow triggers

## Integration Examples

### Flutter Project Integration

For a typical Flutter project structure:

```
my_flutter_app/
├── lib/
├── pubspec.yaml
├── .github/
│   └── workflows/
│       └── bump_version.yaml
└── scripts/
    ├── extract_bump_type.py
    └── flutter_bump_version.py
```

### Custom CI/CD Pipeline

Integrate into any CI/CD system:

```bash
#!/bin/bash
# Custom deployment script

# Extract bump type from commit
COMMIT_MSG=$(git log -1 --pretty=%B)
BUMP_TYPE=$(python3 scripts/extract_bump_type.py "$COMMIT_MSG")

if [ "$BUMP_TYPE" != "error" ]; then
    # Bump version
    python3 scripts/flutter_bump_version.py $BUMP_TYPE
    
    # Build Flutter app
    flutter build apk --release
    
    # Deploy to store
    # ... deployment commands
fi
```

## Version Bumping Logic

### Semantic Versioning Rules

- **Major** (`2.0.0`): Breaking changes, incompatible API changes
- **Minor** (`1.1.0`): New features, backwards compatible
- **Patch** (`1.0.1`): Bug fixes, backwards compatible
- **Build** (`1.0.0+2`): Build metadata, no functional changes

### Build Number Handling

When bumping semantic versions with existing build numbers:

```bash
# Current: 1.0.0+5
python3 flutter_bump_version.py minor
# Result: 1.1.0+6 (increments build number)

# Current: 1.0.0+5  
python3 flutter_bump_version.py build
# Result: 1.0.0+6 (only increments build number)
```

## Error Handling

The Flutter version bumper includes comprehensive error handling:

- **Missing pubspec.yaml**: Clear error message if file not found
- **Invalid version format**: Validates semantic versioning compliance
- **Permission issues**: Handles file access problems gracefully
- **Invalid bump types**: Returns error for unsupported operations

## Examples

### Example 1: New Feature Release

```bash
# Current version in pubspec.yaml: 1.2.3+10
# Commit: "feat(auth): add biometric login Bump:minor"

python3 flutter_bump_version.py minor
# New version: 1.3.0+11
```

### Example 2: Hotfix Release

```bash
# Current version in pubspec.yaml: 2.1.0+25
# Commit: "fix(critical): resolve crash on startup Bump:patch"

python3 flutter_bump_version.py patch  
# New version: 2.1.1+26
```

### Example 3: Build-Only Update

```bash
# Current version in pubspec.yaml: 1.0.0+1
# Internal build for testing

python3 flutter_bump_version.py build
# New version: 1.0.0+2
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure write access to `pubspec.yaml`
2. **Invalid Version Format**: Check that your `pubspec.yaml` uses standard semantic versioning
3. **Workflow Not Triggering**: Verify GitHub Actions permissions and branch protection rules

### Debug Mode

Run with verbose output for troubleshooting:

```bash
python3 flutter_bump_version.py --verbose patch
```

---

*This Flutter-specific version bumping tool ensures your Flutter and Dart projects maintain consistent, automated semantic versioning throughout their development lifecycle.*
