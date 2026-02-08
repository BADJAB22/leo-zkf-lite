# Contributing to LEO-ZKF-Lite

Thank you for your interest in contributing to LEO-ZKF-Lite! We welcome contributions from developers, researchers, and enthusiasts.

## How to Contribute

### 1. Report Bugs
If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Your environment (Python version, OS, etc.)

### 2. Suggest Features
Have an idea? Open an issue with:
- A clear description of the feature
- Why it would be useful
- Potential implementation approach

### 3. Submit Code
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Write or update tests
5. Submit a pull request with a clear description

### 4. Improve Documentation
- Fix typos or unclear explanations
- Add examples or use cases
- Improve API documentation

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/leo-zkf-lite.git
cd leo-zkf-lite

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Run tests
pytest tests/ -v

# Format code
black .

# Check code quality
flake8 .
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all functions
- Keep functions focused and testable

## Testing

All new features should include tests:

```python
# Example test
def test_fragment_verification():
    engine = ZKFLiteEngine(node_id="test-node")
    fragment = engine.create_fragment(
        decision="TEST",
        confidence=0.95,
        local_state_hash="test_hash"
    )
    assert fragment.status == VerificationStatus.PENDING.value
    assert engine.verify_fragment(fragment)
```

## Pull Request Process

1. Update the README if needed
2. Add tests for new functionality
3. Ensure all tests pass: `pytest`
4. Format code: `black .`
5. Check code quality: `flake8 .`
6. Submit PR with a clear description

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Celebrate contributions

## Questions?

Open a discussion or reach out × @baderjamal0

Thank you for making LEO-ZKF-Lite better! 🚀
