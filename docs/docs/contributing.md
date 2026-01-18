# Contributing

Thank you for your interest in contributing to Muwanx! This guide will help you get started.

## Getting Started

### Development Setup

1. **Fork and Clone**

```bash
git clone https://github.com/YOUR_USERNAME/muwanx.git
cd muwanx
```

2. **Create Virtual Environment**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install Development Dependencies**

```bash
pip install -e ".[dev]"
```

4. **Install Pre-commit Hooks**

```bash
pre-commit install
```

## Development Workflow

### Running Tests

```bash
pytest
```

### Code Quality

The project uses several tools to maintain code quality:

- **Ruff**: Linting and formatting
- **Pyright**: Type checking
- **Pre-commit**: Automated checks

Run checks manually:

```bash
# Linting
ruff check .

# Formatting
ruff format .

# Type checking
pyright
```

### Building Documentation

```bash
cd docs
mkdocs serve
```

Then open [http://localhost:8000](http://localhost:8000)

## Project Structure

```
muwanx/
├── src/muwanx/          # Main package
│   ├── __init__.py
│   ├── app.py           # MuwanxApp class
│   ├── builder.py       # Builder class
│   ├── scene.py         # Scene configuration
│   ├── policy.py        # Policy configuration
│   ├── project.py       # Project configuration
│   └── utils.py         # Utility functions
├── tests/               # Test suite
├── examples/            # Example applications
├── docs/                # Documentation
└── pyproject.toml       # Project configuration
```

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

### 2. Make Your Changes

- Write clear, concise code
- Follow existing code style
- Add tests for new features
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run tests
pytest

# Run type checking
pyright

# Run linting
ruff check .

# Format code
ruff format .
```

### 4. Commit Your Changes

Write clear commit messages:

```bash
git add .
git commit -m "Add feature: descriptive message"
```

Good commit message examples:

- `Add support for custom camera angles`
- `Fix policy loading error for large models`
- `Update documentation for Builder.add_project`
- `Refactor scene configuration logic`

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Pull Request Guidelines

### PR Title

Use clear, descriptive titles:

- `Add support for X`
- `Fix issue with Y`
- `Update documentation for Z`

### PR Description

Include:

1. **What** - What does this PR do?
2. **Why** - Why is this change needed?
3. **How** - How does it work?
4. **Testing** - How was it tested?

Example:

```markdown
## What
Adds support for custom camera positions in scenes.

## Why
Users requested ability to set initial camera angles for better
presentation of their models.

## How
- Adds `camera_config` parameter to `SceneConfig`
- Updates builder to pass camera config to client
- Implements camera positioning in three.js viewer

## Testing
- Added unit tests for camera configuration
- Tested with various camera angles
- Verified backward compatibility
```

### Checklist

Before submitting, ensure:

- [ ] Tests pass
- [ ] Code is formatted (ruff)
- [ ] No type errors (pyright)
- [ ] Documentation updated
- [ ] Examples work
- [ ] Commit messages are clear

## Code Style

### Python Style

Follow PEP 8 and project conventions:

```python
# Good
def add_scene(
    model: mujoco.MjModel,
    name: str,
    *,
    initial_qpos: dict[str, float] | None = None
) -> SceneHandle:
    """Add a scene to the project.

    Args:
        model: MuJoCo model for the simulation
        name: Display name for the scene
        initial_qpos: Optional initial joint positions

    Returns:
        Handle for further scene configuration
    """
    pass
```

### Type Hints

Always use type hints:

```python
# Good
def process_config(config: dict[str, Any]) -> ProjectConfig:
    ...

# Not preferred
def process_config(config):
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Brief description of function.

    More detailed description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When something is wrong
    """
    pass
```

## Testing

### Writing Tests

Place tests in the `tests/` directory:

```python
# tests/test_builder.py
import pytest
import muwanx as mwx

def test_builder_creation():
    """Test that Builder can be created."""
    builder = mwx.Builder()
    assert builder is not None

def test_add_project():
    """Test adding a project to builder."""
    builder = mwx.Builder()
    project = builder.add_project(name="Test")
    assert project is not None
    assert len(builder.get_projects()) == 1
```

### Test Coverage

Aim for high test coverage:

```bash
pytest --cov=muwanx
```

## Documentation

### Updating Docs

Documentation is in `docs/source/`:

- User guides: `docs/source/user-guide/`
- API reference: `docs/source/api-reference/`
- Examples: `docs/source/examples/`

### Documentation Style

- Use clear, concise language
- Include code examples
- Add cross-references
- Test all examples

### Building Locally

```bash
cd docs
mkdocs serve
```

## Reporting Issues

### Bug Reports

Include:

1. **Description** - What happened?
2. **Expected** - What should happen?
3. **Steps to Reproduce** - How to reproduce?
4. **Environment** - OS, Python version, etc.
5. **Code** - Minimal example if possible

### Feature Requests

Include:

1. **Use Case** - What are you trying to do?
2. **Proposed Solution** - How should it work?
3. **Alternatives** - What alternatives exist?
4. **Additional Context** - Any other relevant info

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Give constructive feedback
- Focus on what is best for the community

### Communication

- GitHub Issues - Bug reports, feature requests
- GitHub Discussions - Questions, ideas
- Pull Requests - Code contributions

## Recognition

Contributors will be:

- Listed in project contributors
- Credited in release notes
- Acknowledged in documentation

## Questions?

If you have questions:

1. Check existing issues and discussions
2. Review the documentation
3. Ask in GitHub Discussions
4. Open a new issue

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (Apache-2.0).

## Thank You!

Your contributions help make Muwanx better for everyone. Thank you for your time and effort!
