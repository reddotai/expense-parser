# Setup Guide for Non-Technical Users

This guide will get you running in 10 minutes — no coding experience needed.

## Prerequisites

- A computer (Windows, Mac, or Linux)
- Internet connection
- One receipt image (photo or screenshot)

## Step 1: Install Python

### Windows
1. Go to https://python.org/downloads
2. Click "Download Python 3.12"
3. Run the installer
4. **Important:** Check "Add Python to PATH" during installation
5. Click "Install Now"

### Mac
1. Open Terminal (Cmd + Space, type "Terminal")
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

## Step 2: Download This Tool

1. Click the green "Code" button on GitHub
2. Click "Download ZIP"
3. Extract the ZIP file to your Desktop
4. Rename the folder to `expense-parser`

## Step 3: Install Dependencies

### Windows
1. Open Command Prompt
2. Navigate to the folder:
   ```cmd
   cd Desktop\expense-parser
   ```
3. Install requirements:
   ```cmd
   pip install -r requirements.txt
   ```

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

## Step 4: Get an API Key

This tool uses AI to read receipts. You need an API key from OpenAI or Anthropic.

### Option A: OpenAI (Recommended for beginners)

1. Go to https://platform.openai.com/signup
2. Create an account
3. Go to https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)

**Cost:** Approximately $0.01-0.02 per receipt (very affordable)

### Option B: Anthropic (Claude)

1. Go to https://console.anthropic.com/
2. Create an account
3. Get API key (starts with `sk-ant-`)

## Step 5: Set Up Your API Key

1. In the `expense-parser` folder, find `.env.example`
2. Make a copy and rename it to `.env`
3. Open `.env` in any text editor (Notepad, TextEdit)
4. Replace `sk-your-key-here` with your actual API key:
   ```
   OPENAI_API_KEY=sk-abc123youractualkeyhere
   ```
5. Save the file

## Step 6: Configure (Optional)

Open `config.yaml` in a text editor. You can customize:

- **Categories:** Change to match your expense types
- **Currency:** Set to SGD, USD, etc.
- **Output format:** Excel, CSV, or JSON
- **Tax rate:** Singapore GST is 9% (already set)

Don't worry about breaking anything — you can always download the original again.

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

5. Check the `output` folder for your Excel file!

## Troubleshooting

### "pip is not recognized"
- Windows: Reinstall Python and check "Add to PATH"
- Mac: Use `pip3` instead of `pip`

### "No module named 'openai'"
- Run the install command again: `pip install -r requirements.txt`

### "API key not found"
- Check that `.env` file exists (not `.env.example`)
- Verify the key is copied correctly
- Make sure there's no extra space after the key

### "Error processing image"
- Try a clearer photo of the receipt
- Make sure the receipt is readable
- Check your internet connection

## Next Steps

- **Batch processing:** Put multiple receipts in a folder and run: `python parse_receipt.py ./receipts/`
- **Customize categories:** Edit `config.yaml` to match your accounting needs
- **Integrate:** Import the Excel file into your accounting software

## Need Help?

- Open an issue on GitHub
- Email: [your-email@example.com]
- Join our community: [Discord/Slack link]

---

**Remember:** This tool processes receipts locally. Your data stays on your computer unless you choose to share it.
