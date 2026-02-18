# Setup Guide for Non-Technical Users

This guide will get you running in 10 minutes — no coding experience needed.

> 📹 **Prefer video?** Watch our [2-minute setup walkthrough](https://www.youtube.com/your-video-link) (coming soon)

---

## Prerequisites

- A computer (Windows, Mac, or Linux)
- Internet connection
- One receipt image (photo or screenshot)

---

## Quick Start Checklist

Before diving into details, run this quick check:

```bash
python check_setup.py
```

This will tell you if your system is ready or what needs fixing.

---

## Step 1: Install Python

### Windows
1. Go to https://python.org/downloads
2. Click "Download Python 3.12"
3. Run the installer
4. **Important:** Check "Add Python to PATH" during installation  
   > 📸 *[Screenshot: Python installer with "Add to PATH" highlighted]*
5. Click "Install Now"

### Mac
1. Open Terminal (Cmd + Space, type "Terminal")
   > 📸 *[Screenshot: Spotlight search showing Terminal]*
2. Run: `xcode-select --install` (if prompted)
3. Run: `brew install python` (if you have Homebrew)
   
   OR
   
   Download from https://python.org/downloads

### Verify Installation
Open Terminal/Command Prompt and run:
```bash
python --version
```

You should see something like: `Python 3.12.0`

> 📸 *[Screenshot: Terminal showing Python version check]*

**If you see an error**, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for fixes.

---

## Step 2: Download This Tool

1. Click the green "Code" button on GitHub
   > 📸 *[Screenshot: GitHub Code button dropdown]*
2. Click "Download ZIP"
3. Extract the ZIP file to your Desktop
4. Rename the folder to `expense-parser`
   > 📸 *[Screenshot: Desktop showing expense-parser folder]*

---

## Step 3: Install Dependencies

### Windows
1. Open Command Prompt
   > 📸 *[Screenshot: Windows Start menu showing Command Prompt]*
2. Navigate to the folder:
   ```cmd
   cd Desktop\expense-parser
   ```
3. Install requirements:
   ```cmd
   pip install -r requirements.txt
   ```
   > 📸 *[Screenshot: Successful pip install output]*

### Mac
1. Open Terminal
2. Navigate to the folder:
   ```bash
   cd ~/Desktop/expense-parser
   ```
3. Install requirements:
   ```bash
   pip3 install -r requirements.txt
   ```

Wait for installation to complete (2-3 minutes).

**Expected output:**
```
Successfully installed pyyaml pandas pillow openpyxl xlsxwriter pytesseract
```

---

## Step 4: Get an API Key

This tool uses AI to read receipts. You need an API key from OpenAI or Anthropic.

### Option A: OpenAI (Recommended for beginners)

1. Go to https://platform.openai.com/signup
2. Create an account
3. Go to https://platform.openai.com/api-keys
4. Click "Create new secret key"
   > 📸 *[Screenshot: OpenAI API keys page]*
5. Copy the key (starts with `sk-`)

**Cost:** Approximately $0.01-0.02 per receipt (very affordable)

### Option B: Anthropic (Claude)

1. Go to https://console.anthropic.com/
2. Create an account
3. Get API key (starts with `sk-ant-`)

---

## Step 5: Set Up Your API Key

1. In the `expense-parser` folder, find `.env.example`
2. Make a copy and rename it to `.env`
3. Open `.env` in any text editor (Notepad, TextEdit)
   > 📸 *[Screenshot: .env file with API key]*
4. Replace `sk-your-key-here` with your actual API key:
   ```
   OPENAI_API_KEY=sk-abc123youractualkeyhere
   ```
5. Save the file

---

## Step 6: Configure (Optional)

Open `config.yaml` in a text editor. You can customize:

- **Categories:** Change to match your expense types
- **Currency:** Set to SGD, USD, etc.
- **Output format:** Excel, CSV, or JSON
- **Tax rate:** Singapore GST is 9% (already set)

Don't worry about breaking anything — you can always download the original again.

---

## Step 7: Run Your First Receipt

1. Put a receipt image in the `expense-parser` folder
2. Open Terminal/Command Prompt
3. Navigate to the folder (see Step 3)
4. Run:
   ```bash
   # Windows
   python parse_receipt.py receipt.jpg
   
   # Mac
   python3 parse_receipt.py receipt.jpg
   ```
   
   > 📸 *[Screenshot: Terminal showing successful run]*

5. Check the `output` folder for your Excel file!
   > 📸 *[Screenshot: Excel output with extracted data]*

---

## 🎉 Success Checklist

After your first run, verify:

- [ ] Excel file created in `output/` folder
- [ ] File contains: date, vendor, amount, category
- [ ] GST calculated correctly (9% for Singapore)
- [ ] Categories match your config

If all check out, you're ready to batch process!

---

## Troubleshooting

### Common First-Run Issues

| Problem | Quick Fix |
|---------|-----------|
| "python not recognized" | Reinstall Python, check "Add to PATH" |
| "pip not recognized" | Use `python -m pip` instead |
| "No module named 'yaml'" | Run `pip install pyyaml` |
| "API key not found" | Check `.env` file exists and has key |
| "File not found" | Make sure you're in the right folder |

For detailed fixes, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

## Next Steps

- **Batch processing:** Put multiple receipts in a folder and run: `python parse_receipt.py ./receipts/`
- **Customize categories:** Edit `config.yaml` to match your accounting needs
- **Learn more:** Read [HOW_IT_WORKS.md](HOW_IT_WORKS.md) to understand the AI

---

## Need Help?

- 📖 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common errors and fixes
- 🧠 [HOW_IT_WORKS.md](HOW_IT_WORKS.md) — Understanding the AI
- 📚 [LEARNING.md](LEARNING.md) — Deep dive into the code
- 🐛 [Open an Issue](https://github.com/reddotai/expense-parser/issues) — Get help from the community

---

**Remember:** This tool processes receipts locally. Your data stays on your computer unless you choose to share it.
