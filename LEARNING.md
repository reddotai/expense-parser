# Learning Guide: How This Tool Works

Welcome! This guide walks you through the expense-parser codebase, explaining what each part does and why. By the end, you'll understand not just *how* to use it, but *how it works*.

## What You'll Learn

- How AI "reads" images (Computer Vision)
- How we turn unstructured receipts into structured data
- What a "prompt" is and how it shapes AI behavior
- How configuration works (YAML files)
- Basic Python concepts used in this project

---

## The Big Picture: Receipt → Excel

Here's what happens when you run the tool:

```
Your Receipt Image
       ↓
   [AI Vision Model]
       ↓
Extracted Text + Structure
       ↓
   [Python Processing]
       ↓
Formatted Excel/CSV Output
```

Let's break down each step.

---

## Step 1: The AI Vision Model

### What is Computer Vision?

Computer Vision is AI that can "see" and understand images. Just like you can look at a receipt and read the text, AI models can do the same.

### Which AI Model Do We Use?

The tool supports multiple AI providers:
- **OpenAI GPT-4 Vision** — Powerful, requires API key, costs ~$0.01-0.02 per receipt
- **Anthropic Claude** — Alternative to OpenAI, also requires API key
- **Local OCR (Tesseract)** — Free, runs on your computer, less accurate

### How Does the AI "Read" a Receipt?

1. **Image Encoding**: Your receipt image is converted to base64 (a text representation of the image)
2. **API Call**: We send the image to the AI model with instructions
3. **AI Processing**: The model analyzes the image, identifies text, amounts, dates
4. **Structured Response**: The AI returns data in JSON format

### The Prompt: Teaching the AI What to Do

Here's the actual prompt we send (simplified):

```
Extract the following from this receipt image:
1. Vendor/merchant name
2. Date of transaction
3. Items purchased with amounts
4. Subtotal, tax, total
5. Currency
6. Payment method

Return ONLY a JSON object with this structure:
{
    "vendor": "string",
    "date": "DD/MM/YYYY",
    "total": number,
    ...
}
```

**Key Concept**: The prompt is instructions for the AI. Change the prompt, change the output.

---

## Step 2: Python Processing

### File Structure

```
expense-parser/
├── parse_receipt.py      # Main script — this is where the magic happens
├── config.yaml           # Your settings
├── requirements.txt      # Python dependencies
└── output/               # Where Excel files are saved
```

### Key Functions in parse_receipt.py

#### `load_config()`
**What it does**: Reads your `config.yaml` file and turns it into Python data.

**Why it matters**: This is how you customize the tool without changing code.

```python
def load_config(config_path: str = "config.yaml"):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
```

**Learning moment**: YAML is a human-friendly way to write configuration. It's like a settings menu you can edit with a text editor.

---

#### `parse_with_openai()` / `parse_with_anthropic()`
**What it does**: Sends your receipt to the AI and gets back structured data.

**Key steps**:
1. Resize image if too large (AI models have size limits)
2. Encode image to base64
3. Build the prompt with your categories
4. Send API request
5. Parse the JSON response

**Learning moment**: This is where the AI magic happens. The `temperature=0.1` setting means "be deterministic, not creative" — important for data extraction.

---

#### `normalize_vendor()`
**What it does**: Cleans up vendor names using your aliases.

**Example**: "McD" becomes "McDonald's"

**Why it matters**: Consistent vendor names make reporting easier.

---

#### `validate_receipt()`
**What it does**: Checks if extracted data looks reasonable.

**Checks**:
- Is the total amount suspiciously high?
- Is the date in the future?
- Are required fields present?

**Learning moment**: AI isn't perfect. Validation catches obvious errors.

---

#### `save_output()`
**What it does**: Creates Excel/CSV/JSON files from the extracted data.

**Uses**: pandas library for data manipulation, xlsxwriter for Excel formatting.

---

## Step 3: Configuration Deep Dive

### How config.yaml Works

YAML is a markup language that's easy for humans to read and write. Python reads it and turns it into a dictionary (key-value pairs).

```yaml
# This in YAML...
output_format: excel
currency: SGD

# ...becomes this in Python:
{
    "output_format": "excel",
    "currency": "SGD"
}
```

### Key Configuration Options

| Option | What It Controls | Try Changing It |
|--------|------------------|-----------------|
| `output_format` | Excel vs CSV vs JSON | Try "csv" and open in text editor |
| `categories` | Your expense categories | Add "Training & Education" |
| `tax_rate` | GST/VAT percentage | Try 0.08 for 8% |
| `vendor_aliases` | Name normalization | Add your common vendors |

---

## Learning Exercises

### Level 1: Observation (Do This First)

1. Run the tool with `--verbose` flag:
   ```bash
   python parse_receipt.py receipt.jpg --verbose
   ```

2. Look at the output. You should see:
   - Which AI model was used
   - The prompt sent to the AI
   - The raw response
   - Processing time

3. **Question**: What format does the AI return data in?

<details>
<summary>Answer</summary>
JSON (JavaScript Object Notation) — a structured text format that's easy for computers to parse.
</details>

---

### Level 2: Experimentation

1. **Modify the categories**: Add a new category to `config.yaml`, then process a receipt that fits it.

2. **Change the date format**: Try `MM/DD/YYYY` instead of `DD/MM/YYYY`. How does the output change?

3. **Test different vendors**: Add vendor aliases for your most common vendors.

---

### Level 3: Understanding

1. **Read the raw AI response**: Look at the JSON the AI returns. What fields are always present? What's sometimes missing?

2. **Analyze a failure**: Try processing a blurry receipt. What happens? How does the AI handle uncertainty?

3. **Trace the data flow**: Follow a piece of data from receipt image → AI → Excel. What transformations happen?

---

### Level 4: Extension (Advanced)

1. **Add a new output field**: Modify the code to extract "Receipt Number" and add it to the Excel output.

2. **Create a new validation rule**: Add a check for "weekend expenses" and flag them.

3. **Build a simple web UI**: Use Streamlit to create a drag-and-drop interface.

---

## Common Questions

### Q: Why do we need an API key?
**A**: The AI models (GPT-4, Claude) run on cloud servers. The API key is like a password that lets you access them. You pay per use (~1-2 cents per receipt).

### Q: Can I run this without internet?
**A**: Partially. The Tesseract OCR option works offline but is less accurate. For best results, you need internet to call the AI APIs.

### Q: What if the AI gets something wrong?
**A**: Check the confidence score (if using `--verbose`). Low confidence means you should verify manually. You can also modify the prompt to be more specific.

### Q: How do I know which AI model to use?
**A**: 
- **GPT-4 Vision**: Best accuracy, higher cost
- **Claude**: Good alternative, similar cost
- **Tesseract (local)**: Free, lower accuracy, good for testing

---

## Key Concepts Glossary

| Term | Definition |
|------|------------|
| **API** | Application Programming Interface — how programs talk to each other |
| **Base64** | A way to encode binary data (images) as text |
| **JSON** | JavaScript Object Notation — structured data format |
| **LLM** | Large Language Model — AI that understands/generates text |
| **OCR** | Optical Character Recognition — extracting text from images |
| **Prompt** | Instructions given to an AI model |
| **Temperature** | AI setting: 0 = deterministic, 1 = creative |
| **YAML** | Yet Another Markup Language — human-friendly config format |

---

## Next Steps

1. Read `HOW_IT_WORKS.md` for deeper AI concepts
2. Try the exercises above
3. Join our community [link] to share your customizations
4. Check `TROUBLESHOOTING.md` when things go wrong

---

**Remember**: The goal isn't just to run this tool — it's to understand how AI-powered tools are built. Every time you process a receipt, you're using the same technologies that power modern AI applications.

Happy learning! 🎓
