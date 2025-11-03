# Contributing to NETRA

We welcome contributions to the NETRA Facial Recognition System! Here's how you can help:

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure tests pass:
   ```bash
   pytest tests/
   ```

3. Format your code:
   ```bash
   black .
   isort .
   ```

4. Commit your changes with a descriptive message:
   ```bash
   git commit -m "Add new feature: your feature description"
   ```

5. Push to your fork and open a Pull Request

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep functions small and focused on a single responsibility

## Testing

- Write tests for new features and bug fixes
- Ensure all tests pass before submitting a PR
- Add integration tests for new API endpoints

## Pull Request Guidelines

- Keep PRs focused on a single feature or bugfix
- Include a clear description of the changes
- Reference any related issues
- Update documentation as needed

## Reporting Issues

When reporting issues, please include:
- A clear description of the problem
- Steps to reproduce the issue
- Expected vs actual behaviour
- Any relevant error messages or logs

## Code of Conduct

This project adheres to the [Contributor Covenant](https://www.contributor-covenant.org/). By participating, you are expected to uphold this code.
