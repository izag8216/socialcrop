# Contributing to socialcrop

Thank you for your interest in contributing!

## Development Setup

```bash
# Clone and install
git clone https://github.com/izag8216/socialcrop.git
cd socialcrop
pip install -e ".[dev]"
```

## Making Changes

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Run linting: `ruff check src/ tests/`
4. Run tests: `pytest tests/ -v --cov=socialcrop`
5. Ensure coverage stays above 80%
6. Commit with conventional commit format

## Adding Platform Presets

Edit `src/socialcrop/platforms.py` and add a new entry to the `PLATFORMS` dict:

```python
"my-platform": PlatformPreset(
    "My Platform", width, height, "JPEG", "Description (ratio)"
),
```

Then add a test in `tests/test_platforms.py`.

## Reporting Issues

Please open a GitHub issue with:
- Expected behavior
- Actual behavior
- Steps to reproduce
- Python version and OS
