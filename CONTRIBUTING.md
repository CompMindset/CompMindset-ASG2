# Contributing to Rostering App

Thank you for your interest in contributing to the Rostering App! This document provides guidelines for contributing to this project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/CompMindset/CompMindset-ASG2.git
   cd CompMindset-ASG2
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   py -3.9 -m venv .venv
   .venv\Scripts\activate.bat
   
   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   flask initialize
   ```

## Running Tests

Before submitting any changes, ensure all tests pass:

```bash
pytest
```

To run tests with coverage:
```bash
coverage run -m pytest
coverage report
```

## Code Style

- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

## Submitting Changes

1. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

3. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request with a clear description of your changes

## Questions?

If you have questions or need help, please open an issue on GitHub.
