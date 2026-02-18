# How It Works: The AI Behind Expense Parser

Ever wondered how AI can "read" a receipt? This guide explains the technology behind the tool — no computer science degree required.

---

## 🎯 Quick Overview

```
📸 Receipt Photo → 🤖 AI "Reads" It → 📊 Excel Output
      (You)          (The Magic)        (Result)
```

**Time saved**: ~2 minutes per receipt → ~10 seconds

---

## The Core Question: How Does AI Read Receipts?

When you look at a receipt, your brain:
1. **Sees** the image
2. **Recognizes** text (letters, numbers)
3. **Understands** structure (this is the vendor, that's the total)
4. **Extracts** meaning (Starbucks, $12.50, Feb 18)

AI does the same thing, but in a different way.

---

## 📍 Singapore Context

This tool is designed for Singapore professionals:
- **GST**: Automatically calculates 9% (updated 2024)
- **Currency**: SGD by default, auto-detects others
- **Local vendors**: Pre-configured aliases for Grab, NTUC, etc.
- **Date format**: DD/MM/YYYY (Singapore standard)

---

## Method 1: Vision-Language Models (What We Use)

### The Big Idea

Modern AI models like GPT-4 and Claude can look at images AND understand text. They're called "vision-language models" because they process both.

### How It Works (Step by Step)

```
┌─────────────────┐
│  Your Receipt   │  ← A photo or scan
│    (Image)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Image Encoding │  ← Convert to numbers AI understands
│   (Base64)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   AI Analysis   │  ← The model "looks" at the image
│  (GPT-4/Claude) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Structured    │  ← JSON with vendor, date, amounts
│     Output      │
└─────────────────┘
```

### The Magic: The Prompt

We don't just send the image. We send **instructions**:

```
"Look at this receipt image and extract:
- Vendor name
- Date (in DD/MM/YYYY format)
- Total amount
- List of items with prices

Return the result as a JSON object."
```

**Why this matters**: The AI doesn't inherently know what you want. The prompt tells it.

### What is JSON?

JSON (JavaScript Object Notation) is a way to structure data:

```json
{
  "vendor": "Starbucks",
  "date": "18/02/2025",
  "total": 13.95,
  "items": [
    {"description": "Latte", "amount": 6.50},
    {"description": "Croissant", "amount": 6.30}
  ]
}
```

Think of it like a form with labeled fields — easy for computers to read.

---

## Method 2: Traditional OCR (The Alternative)

### What is OCR?

OCR (Optical Character Recognition) is older technology that:
1. **Finds** text in images
2. **Recognizes** what letters/numbers they are
3. **Outputs** plain text

### OCR vs Vision-Language Models

| Feature | Traditional OCR | Vision-Language AI |
|---------|-----------------|-------------------|
| **What it does** | Extracts raw text | Understands meaning |
| **Structure** | Just text | Organized data |
| **Context** | None | Understands "this is a receipt" |
| **Accuracy** | Good on clean text | Better on messy/handwritten |
| **Cost** | Free (Tesseract) | Paid (API calls) |
| **Example** | "Starbucks $12.50 18/2" | `{vendor: "Starbucks", total: 12.50, date: "18/02/2025"}` |

### When to Use Which

- **Use AI (GPT-4/Claude)**: When you need structured data, have messy receipts, want high accuracy
- **Use OCR (Tesseract)**: When you want free local processing, have simple clean receipts, are just testing

---

## Key AI Concepts Explained

### 1. Prompt Engineering

**Definition**: Writing clear instructions for AI models.

**Example**: Compare these prompts:

❌ *Bad*: "Read this receipt"
✅ *Good*: "Extract the vendor name, date (DD/MM/YYYY), and total amount from this receipt. Return as JSON."

**Why it matters**: Better prompts = better results. This is a skill you can learn.

---

### 2. Temperature

**Definition**: How "creative" vs "deterministic" the AI should be.

| Temperature | Use Case |
|-------------|----------|
| **0.0** | Data extraction (what we use) — always same result |
| **0.5** | Balanced — some variation |
| **1.0** | Creative writing — lots of variation |

**Our setting**: `temperature=0.1` — almost deterministic. We want consistent, predictable results for financial data.

---

### 3. Structured Output

**The Problem**: AI can generate any text. We need specific formats.

**The Solution**: Ask for JSON and provide a schema:

```
"Return ONLY a JSON object with this exact structure:
{
  'vendor': 'string',
  'date': 'string',
  'total': number
}"
```

**Why JSON**: Computers can parse it reliably. Excel can import it directly.

---

### 4. Confidence Scores

**The Reality**: AI isn't perfect. Sometimes it's unsure.

**What we show you**:
- **High confidence**: Crystal clear receipt, all fields readable
- **Medium confidence**: Readable but some ambiguity (e.g., handwritten notes)
- **Low confidence**: Blurry, missing info, or unusual format

**How to use confidence scores**:
| Confidence | Action |
|------------|--------|
| High | Trust AI, spot-check |
| Medium | Quick review of key fields (date, total) |
| Low | Full manual review recommended |

**In the output**: Check the "confidence" column in your Excel file.

---

### 5. Hallucination

**Definition**: When AI makes things up.

**Example**: A blurry receipt shows "$12.5" — AI might hallucinate "$125.00"

**How we prevent it**:
- Validation rules (check if totals make sense)
- Low temperature (less creative interpretation)
- Structured output (constrains what AI can return)

---

## The Complete Pipeline

Here's everything that happens when you process a receipt:

### Step 1: Input
- You: Select a receipt image
- System: Validates file format (JPG, PNG, PDF)

### Step 2: Preprocessing
- Resize image if too large (AI has size limits)
- Encode to base64 (text representation)

### Step 3: AI Processing
- Build prompt with your categories
- Send to AI model (OpenAI/Claude)
- Wait for response (1-5 seconds)

### Step 4: Parsing
- Extract JSON from AI response
- Validate structure
- Check for obvious errors

### Step 5: Enrichment
- Normalize vendor names ("McD" → "McDonald's")
- Calculate GST if missing
- Apply your category rules

### Step 6: Output
- Format as Excel/CSV/JSON
- Save to output folder
- (Optional) Show verbose details

---

## Why This Approach?

### The Old Way (Manual)
1. Look at receipt
2. Type into Excel
3. Calculate GST
4. Categorize
5. Save file

**Time**: 2-3 minutes per receipt
**Errors**: Common (typos, wrong categories)

### The New Way (AI-Powered)
1. Take photo of receipt
2. Run tool
3. Review Excel output

**Time**: 10 seconds + 30 seconds review
**Errors**: Rare (AI validation catches most)

**Time saved**: 80-90% reduction in data entry

---

## Limitations (Be Realistic)

### What AI Struggles With

| Challenge | Why | Workaround |
|-----------|-----|------------|
| **Handwritten receipts** | AI trained on printed text | Manual entry or OCR + review |
| **Very blurry images** | Can't read what's not clear | Retake photo, better lighting |
| **Foreign languages** | Model may not understand | Use multilingual models |
| **Complex layouts** | Unusual receipt formats | Manual review |
| **Ambiguous amounts** | "Total" vs "Subtotal" confusion | Validation rules |

### When to Trust AI vs Manual Review

| Confidence | Action |
|------------|--------|
| High (clean receipt, clear text) | Trust AI, spot-check |
| Medium (slightly messy) | Quick review of key fields |
| Low (blurry, unusual) | Full manual review |

---

## Learning Path: From User to Builder

### Level 1: User
- Run the tool
- Customize config.yaml
- Understand the output

### Level 2: Power User
- Use `--verbose` to see AI interactions
- Modify prompts for better accuracy
- Handle edge cases

### Level 3: Customizer
- Add new output fields
- Create custom validation rules
- Build category-specific logic

### Level 4: Builder
- Modify the Python code
- Add new AI providers
- Build extensions (web UI, mobile app)

---

## Try This: Understanding Prompts

1. Open `parse_receipt.py` in a text editor
2. Find the `prompt` variable (around line 100)
3. Read the instructions we send to the AI
4. Try modifying it slightly:
   - Add: "Also extract the cashier name if visible"
   - Change: "Return date in YYYY-MM-DD format"

5. Run the tool and see what changes

**What you learned**: Prompts control AI behavior. Small changes = different outputs.

---

## Further Reading

### Beginner-Friendly
- [How Computer Vision Works (YouTube)](https://youtube.com)
- [Introduction to LLMs](https://example.com)
- [JSON for Non-Programmers](https://example.com)

### Technical Deep Dives
- [OpenAI Vision API Docs](https://platform.openai.com/docs/guides/vision)
- [Claude Vision Capabilities](https://docs.anthropic.com)
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

---

## Summary

**What you should remember**:

1. **AI reads receipts** by converting images to text, then understanding structure
2. **Prompts matter** — they're instructions that shape AI output
3. **JSON is the bridge** between AI understanding and Excel usability
4. **Validation is essential** — AI isn't perfect, checks catch errors
5. **This is just the beginning** — you can extend, customize, and build on this

**The bigger picture**: You're not just automating receipts. You're learning how modern AI applications work — image processing, API calls, structured data, and prompt engineering. These skills apply to countless AI use cases.

---

Questions? Check `LEARNING.md` for hands-on exercises or `TROUBLESHOOTING.md` when things go wrong.
