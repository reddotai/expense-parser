# Example Configurations

Copy any of these to your `config.yaml` or use with `--config` flag.

## Personal Finance (Singapore)

```yaml
output_format: excel
currency: SGD
tax_rate: 0.09
categories:
  - Groceries
  - Dining Out
  - Transport
  - Utilities
  - Entertainment
  - Healthcare
  - Shopping
  - Others

vendor_aliases:
  NTUC: NTUC FairPrice
  "7-11": 7-Eleven
  Grab: Grab Singapore
```

## Small Business (Singapore)

```yaml
output_format: excel
currency: SGD
tax_rate: 0.09
merge_files: monthly
categories:
  - Office Supplies
  - Meals & Entertainment
  - Transport
  - Software & Subscriptions
  - Professional Services
  - Marketing
  - Rent
  - Utilities
  - Equipment
  - Travel

vendor_aliases:
  AWS: Amazon Web Services
  "Google Workspace": Google Cloud
```

## Multi-Currency (Regional Business)

```yaml
output_format: excel
currency: auto
default_currency: SGD
tax_rate: 0.09
categories:
  - Singapore Expenses
  - Malaysia Expenses
  - Indonesia Expenses
  - Thailand Expenses
  - Others

output_columns:
  - date
  - vendor
  - category
  - description
  - subtotal
  - tax
  - total
  - currency
  - sgd_equivalent  # You'd need to add conversion logic
```

## Minimal (Just the Basics)

```yaml
output_format: csv
categories:
  - Business
  - Personal

output_columns:
  - date
  - vendor
  - total
  - category
```

## Maximum Detail

```yaml
output_format: excel
merge_files: false  # Separate file per receipt
categories:
  - Meals & Entertainment
  - Transport
  - Office Supplies
  - Software & Subscriptions
  - Professional Services
  - Marketing & Advertising
  - Utilities
  - Rent
  - Equipment
  - Travel
  - Medical
  - Insurance
  - Training & Education
  - Others

output_columns:
  - date
  - vendor
  - category
  - description
  - items_count
  - subtotal
  - tax
  - total
  - currency
  - payment_method
  - receipt_number
  - file_name
  - processed_at

validation:
  max_amount: 5000
  no_future_dates: true
  max_age_days: 180
  required_fields:
    - date
    - vendor
    - total
```

## Using Custom Configs

```bash
# Use a specific config file
python parse_receipt.py receipt.jpg --config business-config.yaml

# Process with personal settings
python parse_receipt.py ~/Receipts/ --config personal-config.yaml
```
