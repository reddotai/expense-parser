# Expense Parser

Extract structured data from receipt images and PDFs using AI. No coding required to use — just configure and run.

## What This Does

Upload a receipt (photo or PDF). Get a structured Excel/CSV file with:
- Vendor name
- Date
- Items purchased
- Amounts (with tax breakdown)
- Category (auto-detected)
- Payment method

## Quick Start (No Coding)

1. **Install** (one command):
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure** (edit `config.yaml`):
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

3. **Run**:
   ```bash
   python parse_receipt.py receipt.jpg
   ```

4. **Get** `expenses_2025-02-18.xlsx`

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

## Example Output

| Date | Vendor | Category | Description | Subtotal | Tax | Total | Payment |
|------|--------|----------|-------------|----------|-----|-------|---------|
| 18/02/2025 | Starbucks | Meals | Latte & Croissant | 12.80 | 1.15 | 13.95 | Visa |
| 18/02/2025 | Grab | Transport | Ride to client | 18.50 | 0.00 | 18.50 | GrabPay |

## For Non-Technical Users

### Windows
1. Download Python from python.org
2. Open Command Prompt
3. Run `pip install -r requirements.txt`
4. Drag receipt onto `parse_receipt.py`

### Mac
1. Open Terminal
2. Run `pip3 install -r requirements.txt`
3. Run `python3 parse_receipt.py receipt.jpg`

## Advanced: Batch Processing

```bash
# Process entire folder
python parse_receipt.py ./receipts/

# Process with custom config
python parse_receipt.py receipt.jpg --config my-config.yaml
```

## Privacy

- No data leaves your computer
- Uses local AI or your own API key
- No cloud services required

## License

MIT — use freely, modify for your needs.

---

Built by [Better Than SkillsFuture](https://your-substack-link-here) — practical AI tools for Singapore professionals.
