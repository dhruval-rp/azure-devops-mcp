# Contributing Guide

## How to Contribute

1. **Report Issues**
   - Check existing issues first
   - Provide clear description and steps to reproduce
   - Include error messages and logs

2. **Suggest Features**
   - Open an issue with [FEATURE] tag
   - Explain the use case
   - Describe expected behavior

3. **Submit Code**
   - Fork the repository
   - Create a feature branch
   - Follow code style guidelines
   - Test your changes
   - Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone <your-fork-url>
cd TFS

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure .env
cp .env.example .env
# Edit .env with your test credentials
```

## Testing

Before submitting PR:
```bash
# Test connection
python3 test_connection.py

# Test all tools
python3 test_mcp_tools.py
```

## Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions
- Keep functions focused and small
- Add error handling
- Log important operations

## Pull Request Process

1. Update documentation if needed
2. Test all changes thoroughly
3. Ensure no credentials in code
4. Update CHANGELOG if applicable
5. Request review from maintainers

## Questions?

Open an issue or contact the team.
