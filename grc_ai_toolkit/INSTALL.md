# Installation Guide

## Python Version Requirements

**Important**: This toolkit requires **Python 3.10, 3.11, or 3.12**

We recommend **Python 3.11 or 3.12** for best stability and performance.

### Check Your Python Version

```bash
python --version
# or
python3 --version
```

### Install Python (if needed)

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- Choose Python 3.11.x or 3.12.x
- ✅ Check "Add Python to PATH" during installation

**macOS:**
```bash
# Using Homebrew
brew install python@3.12
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.12 python3.12-venv python3.12-dev

# Fedora
sudo dnf install python3.12
```

## Installation Steps

### 1. Create Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd C:\Users\kabra\oceg_grc\grc_ai_toolkit

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install the Toolkit

**For Development (Recommended):**
```bash
pip install -e ".[dev]"
```

This installs:
- Core dependencies (LangChain, OpenAI, Anthropic, etc.)
- Development tools (pytest, black, ruff, mypy)

**For Production Use:**
```bash
pip install .
```

**With All Optional Dependencies:**
```bash
pip install -e ".[all]"
```

This includes local LLM support (transformers, torch).

### 3. Verify Installation

```bash
# Check installation
pip list | grep grc-ai-toolkit

# Run tests
pytest

# Check imports
python -c "from grc_ai_toolkit.llm import LLMManager; print('Success!')"
```

## Configuration

### 1. Set Up Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required: At least one LLM provider
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Configuration
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
```

### 2. Test Your Setup

```python
# test_setup.py
from dotenv import load_dotenv
from grc_ai_toolkit.llm import LLMManager

load_dotenv()

llm = LLMManager()
response = llm.generate("Say 'Hello from GRC AI Toolkit!'")
print(response)
print(f"Cost: ${llm.get_stats()['total_cost']}")
```

Run it:
```bash
python test_setup.py
```

## Common Issues & Solutions

### Issue 1: "ERROR: Unknown compiler(s)" (Windows)

**Problem**: NumPy/other packages trying to build from source.

**Solution**:
```bash
# Use pre-built wheels
pip install --only-binary :all: numpy pandas

# Or upgrade pip first
python -m pip install --upgrade pip setuptools wheel
```

### Issue 2: "No module named 'grc_ai_toolkit'"

**Problem**: Package not installed in current environment.

**Solution**:
```bash
# Make sure you're in the right directory
cd grc_ai_toolkit

# Reinstall in editable mode
pip install -e .
```

### Issue 3: Python Version Mismatch

**Problem**: Using Python 3.14 or 3.9

**Solution**:
```bash
# Check version
python --version

# If wrong version, install Python 3.11 or 3.12
# Then create new venv with correct version:
python3.12 -m venv venv
venv\Scripts\activate
pip install -e ".[dev]"
```

### Issue 4: API Key Errors

**Problem**: "OpenAI API key is required"

**Solution**:
```bash
# Check .env file exists
ls .env  # or dir .env on Windows

# Check it has your key
cat .env  # or type .env on Windows

# Make sure to load dotenv in your code:
from dotenv import load_dotenv
load_dotenv()
```

## Upgrading

### Update to Latest Version

```bash
# Pull latest changes
git pull

# Reinstall with updated dependencies
pip install -e ".[dev]" --upgrade
```

### Clean Reinstall

```bash
# Uninstall
pip uninstall grc-ai-toolkit -y

# Clear cache
pip cache purge

# Reinstall
pip install -e ".[dev]"
```

## Development Setup

### Complete Development Environment

```bash
# 1. Clone repository (if not already done)
cd C:\Users\kabra\oceg_grc

# 2. Create venv with Python 3.11 or 3.12
cd grc_ai_toolkit
python3.12 -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install with dev dependencies
pip install -e ".[dev]"

# 4. Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install

# 5. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 6. Run tests to verify
pytest

# 7. Check code quality
black .
ruff check .
mypy grc_ai_toolkit
```

## Next Steps

After successful installation:

1. **Read the Quick Start** in README.md
2. **Explore Examples**: Check the `examples/` directory (coming soon)
3. **Run Tests**: `pytest -v`
4. **Build Tool 1**: Start implementing the GRC Content Creator

## Getting Help

- **Installation Issues**: Check this guide's troubleshooting section
- **API Issues**: Verify your API keys and quotas
- **Package Issues**: Try `pip install --upgrade pip setuptools wheel`
- **Other Issues**: Open an issue on GitHub

---

**Last Updated**: December 2025
**Supported Python**: 3.10, 3.11, 3.12
**Recommended Python**: 3.11 or 3.12
