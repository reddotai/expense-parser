# Singapore Guide 🇸🇬

Specific guidance for Singapore users — GST, local vendors, and compliance.

---

## GST (Goods and Services Tax)

### Current Rate: 9%

Singapore's GST increased to 9% on 1 January 2024. This is pre-configured in `config.yaml`:

```yaml
tax_rate: 0.09
tax_inclusive: true  # Most Singapore receipts show GST-inclusive prices
```

### GST Treatment Codes

For accounting software integration, receipts may need these IRAS codes:

| Code | Description | When to Use |
|------|-------------|-------------|
| TX | Standard-rated 9% | Most goods and services |
| ZP | Zero-rated 0% | Exports, international services |
| OS | Out-of-scope | Private transactions, non-business |
| BL | Disbursement | Expenses on behalf of client |
| NR | Non-GST registered | Vendor not GST-registered |

### Common GST Scenarios

**Scenario 1: Coffee at Starbucks**
- Total: $5.45
- GST: $0.45 (9%)
- Subtotal: $5.00
- Code: TX

**Scenario 2: Grab Ride**
- Total: $12.00
- GST: $0.00 (transport exempt)
- Code: ZP

**Scenario 3: Hawker Center Meal**
- Total: $4.50
- GST: $0.00 (food exempt)
- Code: ZP

---

## Local Vendor Aliases

Pre-configured in `config.yaml` for common Singapore vendors:

```yaml
vendor_aliases:
  # Food & Beverage
  "McD": "McDonald's Singapore"
  "Macs": "McDonald's Singapore"
  "SB": "Starbucks"
  "KFC": "Kentucky Fried Chicken"
  "7-11": "7-Eleven"
  "7-ELEVEn": "7-Eleven"
  
  # Supermarkets
  "NTUC": "NTUC FairPrice"
  "Fairprice": "NTUC FairPrice"
  "Cold Storage": "Cold Storage (Dairy Farm)"
  "Sheng Siong": "Sheng Siong"
  "Giant": "Giant Singapore"
  
  # Transport
  "Grab": "Grab Singapore"
  "Gojek": "Gojek Singapore"
  "Comfort": "ComfortDelGro"
  "CDG": "ComfortDelGro"
  
  # Telco
  "Singtel": "Singapore Telecommunications"
  "StarHub": "StarHub"
  "M1": "M1 Limited"
  
  # Others
  "Kopitiam": "Kopitiam"
  "Food Republic": "Food Republic"
  "BreadTalk": "BreadTalk"
```

Add your own aliases for frequently used vendors.

---

## Common Singapore Receipt Types

### 1. Kopitiam / Hawker Receipts
**Characteristics**: 
- Often handwritten or thermal paper
- May not show GST separately
- Vendor name might be stall name only

**Tips**:
- Use vendor_aliases to map stall names to proper vendor names
- Check GST applicability (most food is exempt)

### 2. Shopping Mall Receipts
**Characteristics**:
- Usually clear printed receipts
- Show GST separately
- May have multiple items

**Tips**:
- Usually processes well with AI
- Check category_keywords for auto-categorization

### 3. Ride-Hailing (Grab/Gojek)
**Characteristics**:
- E-receipts (screenshots work)
- Transport category
- Usually GST-exempt

**Tips**:
- Screenshot the receipt from app
- Category will auto-detect as "Transport"

### 4. Corporate Expenses
**Characteristics**:
- May require project codes
- Need approval workflows
- Compliance requirements

**Tips**:
- Use custom fields in config for project codes
- Consider adding receipt_number tracking

---

## IRAS Compliance Notes

### Record Keeping Requirements

IRAS requires businesses to keep records for **5 years**.

**What to keep**:
- Original receipt images
- Extracted Excel/CSV files
- Processing logs (if applicable)

**How this tool helps**:
- Original receipts stay on your computer (privacy)
- Excel output includes all required fields
- Timestamped processing for audit trail

### Tax Invoice Requirements

For GST claims, receipts should show:
- ✅ Vendor name and address
- ✅ GST registration number (for claims >$1000)
- ✅ Date of supply
- ✅ Description of goods/services
- ✅ Total amount payable
- ✅ GST amount (if applicable)

**What to do if missing**:
- Request a tax invoice from vendor
- For small amounts (<$1000), simplified tax invoice acceptable
- Keep original receipt + tax invoice together

---

## Singapore-Specific Configuration

Recommended `config.yaml` for Singapore users:

```yaml
# Currency and Tax
currency: SGD
tax_rate: 0.09
tax_inclusive: true
default_currency: SGD

# Categories for Singapore businesses
categories:
  - Meals & Entertainment  # Client meals, team lunches
  - Transport              # Grab, taxi, MRT, petrol
  - Office Supplies        # Stationery, printer ink
  - Software & Subscriptions  # SaaS tools, licenses
  - Professional Services  # Legal, accounting, consulting
  - Marketing & Advertising  # Ads, events, sponsorships
  - Rent                   # Office rent, co-working
  - Utilities              # Electricity, water, internet
  - Equipment              # Laptops, monitors
  - Travel                 # Flights, hotels (overseas)
  - Medical                # Staff medical claims
  - Training & Education   # Courses, certifications
  - Others

# Singapore vendor mappings
vendor_aliases:
  "McD": "McDonald's Singapore"
  "NTUC": "NTUC FairPrice"
  "Grab": "Grab Singapore"
  "Gojek": "Gojek Singapore"
  "Comfort": "ComfortDelGro"
  "Singtel": "Singapore Telecommunications"
  "StarHub": "StarHub Limited"

# Category keywords for Singapore context
category_keywords:
  Meals & Entertainment:
    - restaurant
    - cafe
    - coffee
    - starbucks
    - mcdonald's
    - kfc
    - foodpanda
    - deliveroo
    - grab food
    - kopitiam
    - food republic
    - hawker
  
  Transport:
    - grab
    - gojek
    - taxi
    - comfortdelgro
    - smrt
    - sbs
    - mrt
    - bus
    - petrol
    - esso
    - shell
    - caltex
    - parking
  
  Office Supplies:
    - popular
    - daiso
    - stationery
    - paper
    - printer
  
  Software & Subscriptions:
    - adobe
    - microsoft
    - google
    - slack
    - zoom
    - notion
    - canva
    - github
    - aws

# Output settings
date_format: DD/MM/YYYY  # Singapore standard
output_folder: ./output
merge_files: monthly     # Good for monthly GST filing
```

---

## Integration with Singapore Accounting Software

### Xero

Export format for Xero import:

```yaml
output_format: csv
# Xero requires specific column names
output_columns:
  - date
  - vendor
  - description
  - total
  - gst
  - category
```

Import steps:
1. Process receipts with expense-parser
2. Open CSV in Excel
3. Map columns to Xero fields
4. Import as Bills or Expense Claims

### QuickBooks Singapore

Similar process — export to CSV and import.

### SAP Business One

May require custom formatting. Use JSON output and transform with additional scripting.

---

## FAQs for Singapore Users

**Q: Do I need to charge GST on my expense claims?**
A: No, you're claiming GST paid, not charging it. The tool helps track GST paid for input tax claims.

**Q: What if a receipt doesn't show GST separately?**
A: For most receipts under $1000, this is fine. For larger amounts or if claiming GST, request a tax invoice.

**Q: Can I claim GST on Grab rides?**
A: Transport services are GST-exempt in Singapore, so no GST to claim.

**Q: What about overseas receipts?**
A: Overseas expenses generally don't have Singapore GST. Set `currency: auto` to detect foreign currency.

**Q: How long should I keep receipts?**
A: IRAS requires 5 years. The tool helps by organizing both original images and extracted data.

---

## Need More Help?

- **IRAS GST Guide**: [iras.gov.sg](https://iras.gov.sg)
- **Singapore Accounting Standards**: [isca.org.sg](https://isca.org.sg)
- **Local Support**: [Your community link here]

---

*Last updated: February 2025 (GST rate: 9%)*
