# Troubleshooting Guide

Stuck? Don't worry. This guide covers the most common issues and how to fix them.

---

## Before You Start: Quick Checks

Run these commands to verify your setup:

```bash
# Check Python is installed
python --version
# Should show: Python 3.8+ (or higher)

# Check pip is available
pip --version
# Should show: pip version number

# Check you're in the right folder
pwd
# Should show: .../expense-parser
```

If any of these fail, see the fixes below.

---

## Common Installation Errors

### ❌ Error: "'python' is not recognized"

**What it looks like:**
```
'python' is not recognized as an internal or external command
```

**Why it happens:**
- Python isn't installed, OR
- Python isn't in your system PATH

**Fix for Windows:**
1. Reinstall Python from [python.org](https://python.org)
2. During installation, **CHECK** "Add Python to PATH"
3. Restart Command Prompt
4. Try `python --version` again

**Fix for Mac:**
```bash
# Try python3 instead
python3 --version

# If that works, use python3 for all commands
python3 parse_receipt.py receipt.jpg
```

---

### ❌ Error: "'pip' is not recognized"

**What it looks like:**
```
'pip' is not recognized as an internal or external command
```

**Fix for Windows:**
Same as above — reinstall Python with "Add to PATH" checked.

**Fix for Mac:**
```bash
# Use pip3 instead
pip3 install -r requirements.txt
```

---

### ❌ Error: "Permission denied" when installing

**What it looks like:**
```
PermissionError: [Errno 13] Permission denied
```

**Why it happens:**
You don't have permission to install packages system-wide.

**Fix (all platforms):**
```bash
# Add --user flag to install for your account only
pip install --user -r requirements.txt

# Or use a virtual environment (recommended)
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Then install
pip install -r requirements.txt
```

---

### ❌ Error: "No module named 'yaml'" (or any module)

**What it looks like:**
```
ModuleNotFoundError: No module named 'yaml'
```

**Why it happens:**
The requirements weren't installed properly.

**Fix:**
```bash
# Reinstall requirements
pip install -r requirements.txt

# If that fails, install individually
pip install pyyaml pandas pillow openpyxl xlsxwriter pytesseract
```

---

## Common Runtime Errors

### ❌ Error: "File not found: receipt.jpg"

**What it looks like:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'receipt.jpg'
```

**Why it happens:**
The receipt image isn't in the current folder, or the filename is wrong.

**Fix:**
```bash
# Check what files are in your current folder
ls          # Mac/Linux
dir         # Windows

# Use the full path to your receipt
python parse_receipt.py /Users/yourname/Desktop/receipt.jpg

# Or navigate to where your receipt is
cd /Users/yourname/Desktop
python parse_receipt.py receipt.jpg
```

---

### ❌ Error: "Config file not found"

**What it looks like:**
```
FileNotFoundError: config.yaml not found
```

**Why it happens:**
You're running the script from the wrong folder.

**Fix:**
```bash
# Navigate to the expense-parser folder
cd /path/to/expense-parser

# Then run
python parse_receipt.py receipt.jpg
```

---

### ❌ Error: "OPENAI_API_KEY not set"

**What it looks like:**
```
ValueError: OPENAI_API_KEY environment variable not set
```

**Why it happens:**
You need an API key to use OpenAI's models.

**Fix:**

**Step 1: Get an API key**
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up / log in
3. Go to API Keys → Create new secret key
4. Copy the key (starts with `sk-`)

**Step 2: Set the environment variable**

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

**Mac/Linux:**
```bash
export OPENAI_API_KEY=sk-your-key-here
```

**Step 3: Verify it worked**
```bash
# Windows
echo %OPENAI_API_KEY%

# Mac/Linux
echo $OPENAI_API_KEY
```

**Permanent fix (recommended):**
Create a `.env` file in the expense-parser folder:
```
OPENAI_API_KEY=sk-your-key-here
```

---

### ❌ Error: "Invalid API key"

**What it looks like:**
```
openai.error.AuthenticationError: Invalid API key
```

**Why it happens:**
- Key was copied incorrectly
- Key has been revoked
- You're using the wrong key (use Secret Key, not Publishable Key)

**Fix:**
1. Go back to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new key
3. Copy it carefully (no extra spaces)
4. Set it again

---

### ❌ Error: "Rate limit exceeded"

**What it looks like:**
```
openai.error.RateLimitError: You exceeded your current quota
```

**Why it happens:**
- You've used up your free credits
- You're on a free tier with limits

**Fix:**
1. Check your usage: [platform.openai.com/usage](https://platform.openai.com/usage)
2. Add a payment method to continue
3. Or switch to a different model (Claude, or local OCR)

**Cost note:** Each receipt costs ~$0.01-0.02. 100 receipts = ~$1-2.

---

### ❌ Error: "Connection timeout"

**What it looks like:**
```
TimeoutError: Connection to api.openai.com timed out
```

**Why it happens:**
- Internet connection issue
- Firewall blocking the connection
- OpenAI servers are slow

**Fix:**
1. Check your internet connection
2. Try again in a few minutes
3. Check [OpenAI status](https://status.openai.com)
4. If behind corporate firewall, ask IT to whitelist `api.openai.com`

---

## Receipt Processing Errors

### ❌ Error: "Failed to parse receipt"

**What it looks like:**
```
Error: Failed to parse receipt
```

**Common causes and fixes:**

| Cause | Fix |
|-------|-----|
| **Image too blurry** | Retake photo with better lighting |
| **File format not supported** | Convert to JPG or PNG |
| **Image too large** | The tool auto-resizes, but try compressing first |
| **Receipt is handwritten** | AI struggles with handwriting; try Tesseract mode |
| **Foreign language** | Use a multilingual model or manual entry |

---

### ❌ Error: "TypeError: object of type 'float' has no len()" (Excel Output)

**What it looks like:**
```
TypeError: object of type 'float' has no len()
File "parse_receipt.py", line 456, in save_output
```

**Why it happens:**
This happens when generating Excel output and some data fields are empty (NaN values).

**Fix:**
This bug has been fixed in the latest version. If you still see this error:

1. **Update to the latest version:**
   ```bash
   git pull origin master
   ```

2. **Or use CSV output instead** (works immediately):
   ```bash
   python parse_receipt.py receipt.jpg --format csv
   ```

3. **Or manually patch the code** — open `parse_receipt.py` around line 456 and change:
   ```python
   # OLD (buggy):
   max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
   
   # NEW (fixed):
   col_values = df[col].fillna('').astype(str)
   max_data_len = col_values.map(len).max()
   max_len = max(max_data_len, len(col)) + 2
   ```

---

### ❌ Issue: Output is empty or wrong

**Symptoms:**
- Excel file has blank cells
- Vendor name is wrong
- Amounts don't match

**Fix:**

**Step 1: Run with verbose mode**
```bash
python parse_receipt.py receipt.jpg --verbose
```

**Step 2: Check the AI response**
- Look at what the AI actually extracted
- Compare to the original receipt

**Step 3: Try a different model**
```yaml
# In config.yaml, try a different model
model_provider: anthropic
# or
model_provider: openai
model: gpt-4o  # instead of gpt-4o-mini
```

**Step 4: Manual review**
Some receipts are just hard to read. It's okay to edit the Excel file after.

---

### ❌ Issue: GST calculated wrong

**Symptoms:**
- Tax amount doesn't match receipt
- Total is off by a few cents

**Why:**
- Some receipts include tax in prices
- Some add tax at the end
- Rounding differences

**Fix:**
Check your config:
```yaml
# If receipt shows prices INCLUDING tax
tax_inclusive: true

# If receipt shows prices BEFORE tax
tax_inclusive: false
tax_rate: 0.09  # 9% for Singapore
```

---

## Configuration Errors

### ❌ Error: "YAML syntax error"

**What it looks like:**
```
yaml.scanner.ScannerError: mapping values are not allowed here
```

**Why it happens:**
Your `config.yaml` has a formatting error.

**Common mistakes:**
```yaml
# ❌ Wrong - using tabs instead of spaces
categories:
	- Meals

# ✅ Correct - using spaces
categories:
  - Meals

# ❌ Wrong - missing colon
currency SGD

# ✅ Correct
currency: SGD

# ❌ Wrong - wrong indentation
categories:
- Meals
- Transport

# ✅ Correct
categories:
  - Meals
  - Transport
```

**Fix:**
1. Open `config.yaml` in a text editor
2. Check all lines start with spaces (not tabs)
3. Ensure every setting has `key: value` format
4. Use an online YAML validator if unsure

---

### ❌ Issue: Changes to config not working

**Why:**
You might be editing the wrong file, or the file wasn't saved.

**Fix:**
```bash
# Make sure you're editing the right file
ls config.yaml

# Check the file was modified recently
ls -la config.yaml  # Mac/Linux
dir config.yaml     # Windows
```

---

## Platform-Specific Issues

### Windows-Specific

**Issue: "Windows protected your PC" when installing Python**
- Click "More info" → "Run anyway"

**Issue: Python opens Microsoft Store instead of running**
- Uninstall the "Python" app from Microsoft Store
- Install from [python.org](https://python.org) instead

**Issue: Colors/formatting look weird in Command Prompt**
- This is normal; Windows CMD has limited color support
- Use Windows Terminal for better experience

### Mac-Specific

**Issue: "command not found: python"**
- Use `python3` instead of `python`
- Use `pip3` instead of `pip`

**Issue: "Permission denied" when installing**
- Add `--user` flag: `pip3 install --user -r requirements.txt`

### Linux-Specific

**Issue: Tesseract OCR not found**
```bash
# Install Tesseract
sudo apt-get install tesseract-ocr  # Ubuntu/Debian
sudo yum install tesseract          # CentOS/RHEL
```

---

## Still Stuck?

### Get Help

1. **Check the logs**: Run with `--verbose` and read the full error
2. **Search the error**: Copy the error message into Google
3. **Ask for help**:
   - Open an issue on GitHub
   - Include: error message, what you tried, your operating system

### Provide Good Bug Reports

When asking for help, include:

```
**What I was trying to do:**
Process a receipt image

**What I expected:**
Get an Excel file with extracted data

**What actually happened:**
[Error message here]

**My setup:**
- Operating System: Windows 11 / macOS 14 / Ubuntu 22.04
- Python version: [from python --version]
- Command I ran: [exact command]

**What I've tried:**
[List things you tried from this guide]
```

---

## Quick Reference: Common Commands

```bash
# Check Python
python --version

# Install requirements
pip install -r requirements.txt

# Set API key (Mac/Linux)
export OPENAI_API_KEY=sk-your-key

# Set API key (Windows)
set OPENAI_API_KEY=sk-your-key

# Run the tool
python parse_receipt.py receipt.jpg

# Run with verbose output
python parse_receipt.py receipt.jpg --verbose

# Process a folder
python parse_receipt.py ./receipts/

# Use custom config
python parse_receipt.py receipt.jpg --config my-config.yaml
```

---

## Prevention: Best Practices

✅ **Do:**
- Use a virtual environment
- Keep your API keys in `.env` file (not in code)
- Test with one receipt before batch processing
- Run with `--verbose` when something goes wrong
- Keep receipts as backup (don't delete originals)

❌ **Don't:**
- Share your API keys
- Delete original receipts immediately
- Process hundreds of receipts without testing first
- Ignore warning messages

---

Remember: Errors are normal when learning. Every error message is teaching you something about how the system works. Read them carefully, and you'll get better at debugging.

You've got this! 💪
