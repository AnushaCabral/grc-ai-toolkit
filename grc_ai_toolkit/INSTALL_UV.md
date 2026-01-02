# Installation with uv (Recommended - Modern & Fast)

## Prerequisites

### 1. Install Python 3.12.8

**Download:** https://www.python.org/downloads/release/python-3128/

**Windows Installation:**
1. Download **Windows installer (64-bit)**
2. Run installer
3. ✅ **CHECK "Add Python 3.12 to PATH"** (CRITICAL!)
4. Click "Install Now"

**Verify:**
```bash
python --version
# Should show: Python 3.12.8
```

### 2. Install uv

**Windows (PowerShell - Run as Administrator):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Or via pip (if you prefer):**
```bash
pip install uv
```

**Verify:**
```bash
uv --version
# Should show: uv 0.x.x
```

---

## Installation Steps

### Quick Install (Recommended)

```bash
# 1. Navigate to project
cd C:\Users\kabra\oceg_grc\grc_ai_toolkit

# 2. Create venv and install everything in one command
uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Install package with dev dependencies
uv pip install -e ".[dev]"
```

That's it! ⚡ **Much faster than pip!**

---

## Alternative: Using uv sync

If you add a `uv.lock` file (coming soon):

```bash
# One command to rule them all
uv sync

# Automatically:
# - Creates venv
# - Installs dependencies
# - Handles everything
```

---

## Verify Installation

```bash
# Activate venv
.venv\Scripts\activate

# Check installation
uv pip list | findstr grc

# Run tests
pytest

# Test imports
python -c "from grc_ai_toolkit.llm import LLMManager; print('✅ Success!')"
```

---

## Configuration

### 1. Set up API Keys

```bash
# Copy example
copy .env.example .env

# Edit .env and add your keys
notepad .env
```

Add your keys:
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
LLM_MODEL=gpt-4
```

### 2. Test Setup

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

---

## Common uv Commands

### Package Management

```bash
# Install package
uv pip install package-name

# Install from pyproject.toml
uv pip install -e .

# Install with extras
uv pip install -e ".[dev]"

# Update all packages
uv pip install --upgrade -e ".[dev]"

# Show installed packages
uv pip list

# Show package info
uv pip show grc-ai-toolkit
```

### Virtual Environments

```bash
# Create venv
uv venv

# Create with specific Python version
uv venv --python 3.12

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Deactivate
deactivate
```

### Advanced

```bash
# Install specific version
uv pip install numpy==1.26.4

# Install from requirements file
uv pip install -r requirements.txt

# Freeze current environment
uv pip freeze > requirements-lock.txt

# Check for outdated packages
uv pip list --outdated
```

---

## Speed Comparison

Real-world example from our project:

| Tool | Time | Speed |
|------|------|-------|
| **uv** | ~5 seconds | ⚡⚡⚡⚡⚡ |
| **pip** | ~45 seconds | ⚡ |

**uv is 9x faster!**

---

## Troubleshooting

### Issue: "uv: command not found"

**Solution:**
```bash
# Add to PATH manually (Windows)
# Add this to your PATH:
C:\Users\YourUsername\.cargo\bin

# Or reinstall
pip install uv
```

### Issue: Permission Denied

**Solution:**
```bash
# Run PowerShell as Administrator
# Then reinstall uv
```

### Issue: Still want to use pip?

**No problem!** Everything works with pip too:

```bash
cd C:\Users\kabra\oceg_grc\grc_ai_toolkit
python -m venv venv
venv\Scripts\activate
pip install -e ".[dev]"
```

---

## Why uv is Better

### 1. **Speed** ⚡
- Written in Rust (compiled, not Python)
- Parallel downloads
- Efficient caching
- Smart dependency resolution

### 2. **Better Dependency Resolution**
```bash
# pip might fail with conflicts
pip install package-a package-b
# ERROR: Conflicting dependencies

# uv handles it gracefully
uv pip install package-a package-b
# ✅ Resolved conflicts automatically
```

### 3. **Lock Files** (Coming Soon)
```toml
# uv.lock - ensures everyone has same versions
# Like package-lock.json for Node.js
```

### 4. **Python Version Management**
```bash
# uv can install Python versions too
uv python install 3.12

# Use specific version for venv
uv venv --python 3.12
```

---

## Migration from pip

If you've been using pip:

```bash
# 1. Install uv
pip install uv

# 2. Use uv pip (drop-in replacement)
# OLD: pip install package
# NEW: uv pip install package

# 3. All pip commands work with uv pip
uv pip list
uv pip show package-name
uv pip freeze
uv pip install --upgrade package
```

**It's a drop-in replacement!**

---

## Next Steps

After installation:

1. ✅ Python 3.12.8 installed
2. ✅ uv installed
3. ✅ Virtual environment created
4. ✅ GRC AI Toolkit installed
5. ✅ Tests passing
6. → **Start building Tool 1!**

---

## Resources

- **uv Documentation**: https://docs.astral.sh/uv/
- **uv GitHub**: https://github.com/astral-sh/uv
- **Python 3.12 Docs**: https://docs.python.org/3.12/

---

**Updated**: December 2025
**Python Version**: 3.12.8
**Package Manager**: uv (recommended) or pip
