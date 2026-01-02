#!/usr/bin/env python
"""
Python Version Checker for GRC AI Toolkit

Run this script to verify your Python version is compatible.
"""

import sys


def check_python_version():
    """Check if Python version is compatible"""

    version_info = sys.version_info
    version_str = f"{version_info.major}.{version_info.minor}.{version_info.micro}"

    print("=" * 60)
    print("GRC AI Toolkit - Python Version Check")
    print("=" * 60)
    print(f"\nYour Python Version: {version_str}")
    print(f"Python Executable: {sys.executable}")

    # Check major version
    if version_info.major != 3:
        print("\n❌ ERROR: Python 3 is required")
        print(f"   You are using Python {version_info.major}")
        print("\n   Please install Python 3.11 or 3.12")
        return False

    # Check minor version
    if version_info.minor < 10:
        print(f"\n❌ ERROR: Python 3.10 or higher is required")
        print(f"   You are using Python {version_str}")
        print("\n   Please upgrade to Python 3.11 or 3.12")
        return False

    if version_info.minor >= 13:
        print(f"\n⚠️  WARNING: Python {version_str} is very new")
        print("   Recommended versions: 3.11 or 3.12")
        print("   Some dependencies may not have pre-built wheels yet")
        print("\n   Consider using Python 3.11 or 3.12 for best compatibility")
        return False

    # Version is good
    if version_info.minor in [11, 12]:
        print(f"\n✅ EXCELLENT: Python {version_str} is recommended!")
    else:
        print(f"\n✅ OK: Python {version_str} is compatible")

    print("\nYou can proceed with installation:")
    print("   pip install -e \".[dev]\"")

    return True


def check_pip():
    """Check pip version"""
    try:
        import pip
        print(f"\n📦 pip version: {pip.__version__}")
    except:
        print("\n⚠️  WARNING: pip not found")
        print("   Install pip: python -m ensurepip --upgrade")


def check_venv():
    """Check if running in virtual environment"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

    if in_venv:
        print("\n🔒 Virtual Environment: Active")
        print(f"   Location: {sys.prefix}")
    else:
        print("\n⚠️  Virtual Environment: Not Active")
        print("\n   Recommended: Create and activate a virtual environment")
        print("   Windows: python -m venv venv && venv\\Scripts\\activate")
        print("   macOS/Linux: python -m venv venv && source venv/bin/activate")


if __name__ == "__main__":
    print()
    is_compatible = check_python_version()
    check_pip()
    check_venv()

    print("\n" + "=" * 60)

    if is_compatible:
        print("✅ Ready to install GRC AI Toolkit!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ Please fix the issues above before installation")
        print("=" * 60)
        sys.exit(1)
