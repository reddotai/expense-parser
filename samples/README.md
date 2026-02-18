# Sample Receipts

This folder contains sample receipt images for testing the expense parser.

## Included Samples

| File | Description | Difficulty | Expected Output |
|------|-------------|------------|-----------------|
| `receipt-starbucks.jpg` | Clean printed receipt | Easy | Clear extraction |
| `receipt-ntuc.jpg` | Singapore supermarket receipt | Medium | GST handling |
| `receipt-grab.jpg` | Grab ride receipt | Easy | Transport category |
| `receipt-blurry.jpg` | Intentionally blurry | Hard | May need review |

## Using Samples

Test the tool without using your own receipts:

```bash
python parse_receipt.py samples/receipt-starbucks.jpg --verbose
```

## Expected Results

### Starbucks Receipt
- **Vendor**: Starbucks
- **Category**: Meals & Entertainment
- **Items**: Coffee, pastry
- **GST**: 9% (Singapore)

### NTUC Receipt
- **Vendor**: NTUC FairPrice
- **Category**: Groceries
- **GST**: 9% on applicable items

### Grab Receipt
- **Vendor**: Grab Singapore
- **Category**: Transport
- **GST**: May not apply to transport

## Learning Exercise

Compare the outputs:

1. Run with `--verbose` on each sample
2. Observe how the AI handles different receipt formats
3. Check the confidence of extraction
4. Note which fields are sometimes missing

This helps you understand what makes a "good" receipt for AI processing.
