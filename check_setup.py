#!/usr/bin/env python3
"""
Setup Checker for Expense Parser
Run this before starting to verify your environment is ready.
"""

import sys
import subprocess
import os
from pathlib import Path


def check_python():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        return True, f"✅ Python {version.major}.{version.minor}.{version.micro}"
    return False, f"❌ Python {version.major}.{version.minor} (need 3.8+)"


def check_pip():
    """Check pip is available."""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return True, f"✅ {result.stdout.strip()}"
        return False, "❌ pip not found"
    except Exception as e:
        return False, f"❌ pip check failed: {e}"


def check_dependencies():
    """Check if required packages are installed."""
    required = ['yaml', 'pandas', 'PIL', 'openpyxl', 'xlsxwriter']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if not missing:
        return True, "✅ All required packages installed"
    return False, f"❌ Missing packages: {', '.join(missing)}\n   Run: pip install -r requirements.txt"


def check_api_key():
    """Check if API key is set."""
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    if openai_key or anthropic_key:
        provider = "OpenAI" if openai_key else "Anthropic"
        return True, f"✅ {provider} API key found"
    return False, "⚠️  No API key found (optional - you can use local OCR)\n   Set with: export OPENAI_API_KEY=sk-your-key"


def check_config():
    """Check if config.yaml exists."""
    if Path('config.yaml').exists():
        return True, "✅ config.yaml found"
    return False, "❌ config.yaml not found\n   Copy from: cp config.yaml.example config.yaml"


def check_receipts_folder():
    """Check for receipt files."""
    receipt_dirs = ['.', './receipts', './samples']
    found_receipts = []
    
    for dir_path in receipt_dirs:
        if Path(dir_path).exists():
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.pdf']:
                found_receipts.extend(Path(dir_path).glob(ext))
    
    if found_receipts:
        return True, f"✅ Found {len(found_receipts)} receipt(s) to test with"
    return False, "⚠️  No receipt images found\n   Add receipt images to process"


def main():
    """Run all checks."""
    print("🔍 Expense Parser Setup Checker\n")
    print("Checking your environment...\n")
    
    checks = [
        ("Python 3.8+", check_python),
        ("pip (package manager)", check_pip),
        ("Required packages", check_dependencies),
        ("API key (optional)", check_api_key),
        ("Configuration file", check_config),
        ("Receipt images", check_receipts_folder),
    ]
    
    results = []
    for name, check_func in checks:
        status, message = check_func()
        results.append((name, status, message))
        print(message)
    
    # Summary
    print("\n" + "="*50)
    passed = sum(1 for _, status, _ in results if status)
    total = len(results)
    
    if passed == total:
        print("🎉 All checks passed! You're ready to go.")
        print("\nNext steps:")
        print("  1. Review config.yaml and customize for your needs")
        print("  2. Run: python parse_receipt.py receipt.jpg")
        print("  3. Check the output/ folder for results")
        return 0
    elif passed >= total - 1:  # Allow API key to be optional
        print(f"⚠️  {passed}/{total} checks passed (API key is optional)")
        print("\nYou can proceed with local OCR, or set an API key for better accuracy:")
        print("  export OPENAI_API_KEY=sk-your-key")
        return 0
    else:
        print(f"❌ {passed}/{total} checks passed")
        print("\nPlease fix the issues above before continuing.")
        print("\nNeed help? See:")
        print("  - SETUP.md for detailed setup instructions")
        print("  - TROUBLESHOOTING.md for common errors")
        return 1


if __name__ == '__main__':
    sys.exit(main())
