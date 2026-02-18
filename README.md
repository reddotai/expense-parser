# Expense Parser

Extract structured data from receipt images and PDFs using AI. **This is a learning project** — you'll learn how AI tools work by building something useful.

> 🎓 **New to AI?** Start with [HOW_IT_WORKS.md](HOW_IT_WORKS.md) to understand the technology, then [LEARNING.md](LEARNING.md) for hands-on exercises.

---

## What This Does

Upload a receipt (photo or PDF). Get a structured Excel/CSV file with:
- Vendor name
- Date
- Items purchased
- Amounts (with tax breakdown)
- Category (auto-detected)
- Payment method

**The AI magic**: The tool uses vision-language models (like GPT-4) to "read" your receipt and extract structured data — no manual typing required.

---

## Before You Start

### ✅ Checklist

- [ ] **Python 3.8+ installed** — [Download here](https://python.org) (free)
- [ ] **Can open Terminal/Command Prompt** — See [SETUP.md](SETUP.md) for help
- [ ] **Have a receipt image ready** — Photo or screenshot works
- [ ] **OpenAI API key** — [Get one free](https://platform.openai.com) (includes $5 credit)

### 🆘 New to command line?

Don't worry! This project is designed for beginners. If you get stuck, check:
- [SETUP.md](SETUP.md) — Step-by-step setup guide with screenshots
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common errors and fixes
- [LEARNING.md](LEARNING.md) — Understanding what each step does

---

## Quick Start

### 1. Install

```bash
pip install -r requirements.txt
```

**What this does**: Downloads the Python libraries this tool needs to run.

### 2. Configure

Edit `config.yaml`:

```yaml
output_format: excel        # excel, csv, or json
currency: SGD               # Auto-detect or specify
categories:                 # Customize for your needs
  - Meals & Entertainment
  - Transport
  - Office Supplies
  - Software
  - Professional Services
```

**What this does**: Tells the tool your preferences — no coding needed.

### 3. Set API Key

**Mac/Linux:**
```bash
export OPENAI_API_KEY=sk-your-key-here
```

**Windows:**
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

**What this does**: Gives the tool access to AI models (costs ~$0.01 per receipt).

### 4. Run

```bash
python parse_receipt.py receipt.jpg
```

**What this does**: Sends your receipt to AI, gets back structured data, saves to Excel.

### 5. See Results

Check the `output/` folder for your Excel file!

---

## Learn As You Go

### 📚 Documentation

| File | What's Inside |
|------|---------------|
| [HOW_IT_WORKS.md](HOW_IT_WORKS.md) | How AI reads receipts, what is OCR, what are prompts |
| [LEARNING.md](LEARNING.md) | Code walkthrough, learning exercises, key concepts |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common errors and how to fix them |
| [SETUP.md](SETUP.md) | Detailed setup for Windows/Mac |
| [EXAMPLES.md](EXAMPLES.md) | Sample configurations for different use cases |

### 🎯 Learning Path

**Level 1: Get It Working** (15 min)
- Follow Quick Start above
- Process your first receipt
- Celebrate! 🎉

**Level 2: Understand It** (30 min)
- Read [HOW_IT_WORKS.md](HOW_IT_WORKS.md)
- Run with `--verbose` to see AI in action:
  ```bash
  python parse_receipt.py receipt.jpg --verbose
  ```
- Customize your categories

**Level 3: Customize It** (1 hour)
- Read [LEARNING.md](LEARNING.md)
- Try the exercises
- Modify the config for your workflow

**Level 4: Extend It** (ongoing)
- Modify the code
- Add new features
- Share your improvements

---

## User Configuration Options

All customization happens in `config.yaml` — no code changes needed:

| Option | Description | Default |
|--------|-------------|---------|
| `output_format` | excel / csv / json | excel |
| `currency` | Auto-detect or SGD/USD/etc | auto |
| `categories` | Your expense categories | See config.yaml |
| `tax_rate` | GST/VAT rate for your region | 0.09 (9% Singapore GST) |
| `date_format` | How dates appear in output | DD/MM/YYYY |
| `output_folder` | Where to save files | ./output |
| `merge_files` | Combine all into one file | false (daily files) |
| `vendor_aliases` | Map "McD" → "McDonald's" | {} |

---

## Example Output

| Date | Vendor | Category | Description | Subtotal | Tax | Total | Payment |
|------|--------|----------|-------------|----------|-----|-------|---------|
| 18/02/2025 | Starbucks | Meals | Latte & Croissant | 12.80 | 1.15 | 13.95 | Visa |
| 18/02/2025 | Grab | Transport | Ride to client | 18.50 | 0.00 | 18.50 | GrabPay |

---

## Advanced Usage

### Batch Processing

```bash
# Process entire folder
python parse_receipt.py ./receipts/

# Process with custom config
python parse_receipt.py receipt.jpg --config my-config.yaml

# See detailed processing info
python parse_receipt.py receipt.jpg --verbose
```

### Different AI Models

```yaml
# In config.yaml

# Option 1: OpenAI (recommended)
model_provider: openai
model: gpt-4o-mini  # Fast, cheap, accurate

# Option 2: Anthropic Claude
model_provider: anthropic
model: claude-3-haiku-20240307

# Option 3: Local OCR (free, no API key, less accurate)
model_provider: local
```

---

## What You'll Learn

By completing this project, you'll understand:

- ✅ How AI "reads" images (Computer Vision)
- ✅ What OCR is and how it works
- ✅ How to configure software without coding
- ✅ Basic command-line usage
- ✅ How AI processes unstructured data into structured formats
- ✅ What prompts are and how they shape AI behavior

**This is the foundation for building your own AI tools.**

---

## Privacy & Security

- ✅ **No data leaves your computer** (unless using cloud AI APIs)
- ✅ **Local processing option** available (Tesseract OCR)
- ✅ **You control your API keys** — we never see them
- ✅ **Open source** — inspect the code, no hidden data collection

---

## Need Help?

| Problem | Solution |
|---------|----------|
| Stuck on setup | [SETUP.md](SETUP.md) |
| Error message | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| Want to understand AI | [HOW_IT_WORKS.md](HOW_IT_WORKS.md) |
| Want to modify code | [LEARNING.md](LEARNING.md) |
| Something else | Open a GitHub Issue |

---

## License

MIT — use freely, modify for your needs.

---

Built by [Better Than SkillsFuture](https://your-substack-link-here) — practical AI upskilling for Singapore professionals.

**Not just using AI. Understanding AI.** 🚀
