#!/usr/bin/env python3
"""
Expense Parser - Extract structured data from receipts
No coding required - just configure config.yaml and run!
"""

import os
import sys
import json
import argparse
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import base64

import yaml
import pandas as pd
from PIL import Image
import pytesseract

# Try to import optional dependencies
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load user configuration from YAML file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def encode_image(image_path: str) -> str:
    """Encode image to base64 for API calls."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def resize_image(image_path: str, max_size: int = 4096, quality: str = "medium") -> str:
    """Resize image if too large, return path to resized image."""
    img = Image.open(image_path)
    
    # Quality settings
    quality_map = {"low": 1024, "medium": 2048, "high": 4096}
    target_size = quality_map.get(quality, 2048)
    
    # Resize if needed
    max_dim = max(img.size)
    if max_dim > max_size:
        ratio = max_size / max_dim
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # Save to temp
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"resized_{os.path.basename(image_path)}")
    img.save(temp_path, quality=95)
    return temp_path


def extract_text_tesseract(image_path: str) -> str:
    """Extract text from image using Tesseract OCR (local, no API)."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text


def parse_with_openai(image_path: str, config: Dict[str, Any], api_key: str, verbose: bool = False) -> Dict[str, Any]:
    """Parse receipt using OpenAI Vision API."""
    client = openai.OpenAI(api_key=api_key)
    
    # Resize image
    resized_path = resize_image(
        image_path, 
        config.get('max_image_size', 4096),
        config.get('image_quality', 'medium')
    )
    base64_image = encode_image(resized_path)
    
    # Build category list
    categories = config.get('categories', [])
    category_list = ", ".join(categories)
    
    # Build prompt with confidence instruction
    prompt = f"""Extract the following information from this receipt image:
    
1. Vendor/merchant name
2. Date of transaction (format: DD/MM/YYYY)
3. Items purchased (list with descriptions and amounts)
4. Subtotal (before tax)
5. Tax amount (GST/VAT)
6. Total amount
7. Currency (SGD, USD, etc.)
8. Payment method (Cash, Visa, Mastercard, GrabPay, etc.)
9. Receipt/transaction number if visible
10. Confidence score (high/medium/low) based on clarity of extraction

Classify the expense into ONE of these categories: {category_list}

Return ONLY a JSON object with this exact structure:
{{
    "vendor": "string",
    "date": "DD/MM/YYYY",
    "category": "string",
    "items": [
        {{"description": "string", "amount": number}}
    ],
    "subtotal": number,
    "tax": number,
    "total": number,
    "currency": "string",
    "payment_method": "string",
    "receipt_number": "string or null",
    "confidence": "high|medium|low"
}}

If any field is not visible, use null or 0. Be precise with numbers.
Set confidence based on: high=crystal clear, medium=readable but some ambiguity, low=hard to read or missing info."""

    response = client.chat.completions.create(
        model=config.get('model', 'gpt-4o-mini'),
        temperature=config.get('temperature', 0.1),
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )
    
    # Parse JSON response
    content = response.choices[0].message.content
    # Extract JSON from markdown code block if present
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]
    
    return json.loads(content.strip())


def parse_with_anthropic(image_path: str, config: Dict[str, Any], api_key: str, verbose: bool = False) -> Dict[str, Any]:
    """Parse receipt using Anthropic Claude Vision API."""
    client = anthropic.Anthropic(api_key=api_key)
    
    # Resize and encode
    resized_path = resize_image(
        image_path,
        config.get('max_image_size', 4096),
        config.get('image_quality', 'medium')
    )
    base64_image = encode_image(resized_path)
    
    categories = config.get('categories', [])
    category_list = ", ".join(categories)
    
    prompt = f"""Extract the following information from this receipt image:
    
1. Vendor/merchant name
2. Date of transaction (format: DD/MM/YYYY)
3. Items purchased (list with descriptions and amounts)
4. Subtotal (before tax)
5. Tax amount (GST/VAT)
6. Total amount
7. Currency (SGD, USD, etc.)
8. Payment method (Cash, Visa, Mastercard, GrabPay, etc.)
9. Receipt/transaction number if visible
10. Confidence score (high/medium/low) based on clarity of extraction

Classify the expense into ONE of these categories: {category_list}

Return ONLY a JSON object with this exact structure:
{{
    "vendor": "string",
    "date": "DD/MM/YYYY",
    "category": "string",
    "items": [
        {{"description": "string", "amount": number}}
    ],
    "subtotal": number,
    "tax": number,
    "total": number,
    "currency": "string",
    "payment_method": "string",
    "receipt_number": "string or null",
    "confidence": "high|medium|low"
}}

If any field is not visible, use null or 0. Be precise with numbers.
Set confidence based on: high=crystal clear, medium=readable but some ambiguity, low=hard to read or missing info."""

    response = client.messages.create(
        model=config.get('model', 'claude-3-haiku-20240307'),
        max_tokens=4096,
        temperature=config.get('temperature', 0.1),
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64_image
                        }
                    }
                ]
            }
        ]
    )
    
    content = response.content[0].text
    # Extract JSON from markdown if present
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]
    
    return json.loads(content.strip())


def parse_receipt(image_path: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Parse a single receipt using configured AI model."""
    provider = config.get('model_provider', 'openai')
    
    # Get API key from environment
    if provider == 'openai':
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        return parse_with_openai(image_path, config, api_key)
    
    elif provider == 'anthropic':
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        return parse_with_anthropic(image_path, config, api_key)
    
    else:
        raise ValueError(f"Unknown model provider: {provider}")


def normalize_vendor(vendor: str, aliases: Dict[str, str]) -> str:
    """Normalize vendor name using aliases."""
    if not vendor:
        return vendor
    
    vendor_clean = vendor.strip()
    # Check for exact match
    if vendor_clean in aliases:
        return aliases[vendor_clean]
    # Check case-insensitive
    for alias, full_name in aliases.items():
        if vendor_clean.lower() == alias.lower():
            return full_name
    return vendor_clean


def validate_receipt(data: Dict[str, Any], config: Dict[str, Any]) -> List[str]:
    """Validate extracted data against rules."""
    warnings = []
    validation = config.get('validation', {})
    
    # Check required fields
    required = validation.get('required_fields', [])
    for field in required:
        if field not in data or data[field] is None:
            warnings.append(f"Missing required field: {field}")
    
    # Check max amount
    max_amount = validation.get('max_amount', 10000)
    if data.get('total', 0) > max_amount:
        warnings.append(f"Total exceeds {max_amount}: {data['total']}")
    
    # Check date
    if validation.get('no_future_dates', True):
        try:
            receipt_date = datetime.strptime(data.get('date', ''), '%d/%m/%Y')
            if receipt_date > datetime.now():
                warnings.append("Date is in the future")
        except:
            pass
    
    return warnings


def format_output(data: Dict[str, Any], config: Dict[str, Any], filename: str) -> Dict[str, Any]:
    """Format parsed data for output."""
    # Normalize vendor
    aliases = config.get('vendor_aliases', {})
    data['vendor'] = normalize_vendor(data.get('vendor', ''), aliases)
    
    # Add metadata
    data['file_name'] = filename
    data['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['items_count'] = len(data.get('items', []))
    
    # Set default currency if missing
    if not data.get('currency'):
        data['currency'] = config.get('default_currency', 'SGD')
    
    return data


def save_output(records: List[Dict[str, Any]], config: Dict[str, Any]):
    """Save parsed records to file."""
    output_folder = config.get('output_folder', './output')
    os.makedirs(output_folder, exist_ok=True)
    
    # Determine filename based on merge strategy
    merge_strategy = config.get('merge_files', 'daily')
    date_format = config.get('date_format', 'DD/MM/YYYY')
    
    if merge_strategy == 'single':
        filename = 'expenses_all.xlsx'
    elif merge_strategy == 'daily':
        filename = f"expenses_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    elif merge_strategy == 'weekly':
        filename = f"expenses_week_{datetime.now().strftime('%Y-W%U')}.xlsx"
    elif merge_strategy == 'monthly':
        filename = f"expenses_{datetime.now().strftime('%Y-%m')}.xlsx"
    else:
        filename = f"expenses_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    
    output_path = os.path.join(output_folder, filename)
    
    # Create DataFrame
    df = pd.DataFrame(records)
    
    # Reorder columns based on config
    columns = config.get('output_columns', [])
    if columns:
        # Only include columns that exist
        available_cols = [c for c in columns if c in df.columns]
        df = df[available_cols]
    
    # Save based on format
    output_format = config.get('output_format', 'excel')
    
    if output_format == 'excel':
        # Use xlsxwriter for better formatting
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Expenses', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Expenses']
            for i, col in enumerate(df.columns):
                max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, min(max_len, 50))
    
    elif output_format == 'csv':
        output_path = output_path.replace('.xlsx', '.csv')
        df.to_csv(output_path, index=False)
    
    elif output_format == 'json':
        output_path = output_path.replace('.xlsx', '.json')
        with open(output_path, 'w') as f:
            json.dump(records, f, indent=2)
    
    print(f"✓ Saved {len(records)} receipts to: {output_path}")
    
    # Generate IRAS export if enabled
    iras_config = config.get('iras_export', {})
    if iras_config.get('enabled', False):
        iras_path = save_iras_export(records, config, output_folder)
        print(f"✓ IRAS GST export: {iras_path}")
    
    return output_path


def save_iras_export(records: List[Dict[str, Any]], config: Dict[str, Any], output_folder: str):
    """Save records in IRAS GST F5-compatible format."""
    iras_config = config.get('iras_export', {})
    default_code = iras_config.get('default_gst_code', 'TX')
    category_codes = iras_config.get('category_gst_codes', {})
    
    # Map records to IRAS format
    iras_records = []
    for record in records:
        category = record.get('category', 'Others')
        gst_code = category_codes.get(category, default_code)
        
        # Calculate GST amount
        subtotal = record.get('subtotal', 0) or record.get('total', 0)
        tax = record.get('tax', 0)
        total = record.get('total', 0)
        
        # For zero-rated or out-of-scope, adjust
        if gst_code in ['ZP', 'OS']:
            tax = 0
        
        iras_records.append({
            'Date': record.get('date', ''),
            'Supplier Name': record.get('vendor', ''),
            'Supplier GST Reg No': '',  # Would need to be extracted or mapped
            'Description': record.get('description', ''),
            'Value Excl GST': subtotal,
            'GST Amount': tax,
            'Total Amount': total,
            'GST Code': gst_code,
            'Receipt Reference': record.get('receipt_number', ''),
        })
    
    # Save as CSV
    df = pd.DataFrame(iras_records)
    iras_path = os.path.join(output_folder, f"iras_gst_export_{datetime.now().strftime('%Y-%m-%d')}.csv")
    df.to_csv(iras_path, index=False)
    
    return iras_path


def main():
    parser = argparse.ArgumentParser(
        description='Extract structured data from receipt images'
    )
    parser.add_argument(
        'input',
        help='Receipt image file or folder containing images'
    )
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to config file (default: config.yaml)'
    )
    parser.add_argument(
        '--output',
        help='Override output folder'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed processing information'
    )
    parser.add_argument(
        '--confidence-threshold',
        default='medium',
        choices=['high', 'medium', 'low'],
        help='Minimum confidence level to accept (default: medium)'
    )
    
    args = parser.parse_args()
    
    # Load config
    if args.verbose:
        print(f"🔧 Loading config from: {args.config}")
    config = load_config(args.config)
    
    if args.verbose:
        print(f"⚙️  Settings: {json.dumps(config, indent=2)}")
    
    if args.output:
        config['output_folder'] = args.output
    
    # Get input files
    input_path = Path(args.input)
    if input_path.is_dir():
        # Get all image files
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.pdf']
        files = []
        for ext in extensions:
            files.extend(input_path.glob(ext))
            files.extend(input_path.glob(ext.upper()))
        files = list(set(files))  # Remove duplicates
    else:
        files = [input_path]
    
    if not files:
        print("No receipt files found!")
        sys.exit(1)
    
    print(f"Found {len(files)} receipt(s) to process")
    if args.verbose:
        print(f"📁 Files: {[f.name for f in files]}")
    
    # Process each receipt
    records = []
    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {file_path.name}")
        
        if args.verbose:
            print(f"🖼️  Image: {file_path}")
        
        try:
            # Parse receipt
            data = parse_receipt(str(file_path), config)
            
            if args.verbose:
                print(f"📊 Raw extraction: {json.dumps(data, indent=2)}")
            
            # Validate
            warnings = validate_receipt(data, config)
            if warnings:
                print(f"  ⚠ Warnings: {', '.join(warnings)}")
            
            # Format
            formatted = format_output(data, config, file_path.name)
            
            # Check confidence
            confidence = formatted.get('confidence', 'medium')
            threshold_map = {'high': 3, 'medium': 2, 'low': 1}
            confidence_map = {'high': 3, 'medium': 2, 'low': 1}
            
            if confidence_map.get(confidence, 2) < threshold_map.get(args.confidence_threshold, 2):
                print(f"  ⚠ Low confidence ({confidence}) - review recommended")
            elif confidence == 'low':
                print(f"  ⚠ Low confidence - review recommended")
            else:
                print(f"  ✓ Confidence: {confidence}")
            
            records.append(formatted)
            
            print(f"    {formatted.get('vendor', 'Unknown')} - ${formatted.get('total', 0):.2f}")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            continue
    
    # Save output
    if records:
        output_path = save_output(records, config)
        
        # Summary
        low_confidence = [r for r in records if r.get('confidence') == 'low']
        medium_confidence = [r for r in records if r.get('confidence') == 'medium']
        
        print(f"\n✓ Done! Processed {len(records)} receipt(s)")
        print(f"  High confidence: {len(records) - len(low_confidence) - len(medium_confidence)}")
        if medium_confidence:
            print(f"  Medium confidence: {len(medium_confidence)} (quick review recommended)")
        if low_confidence:
            print(f"  ⚠ Low confidence: {len(low_confidence)} (detailed review needed)")
            print(f"    Files: {', '.join(r.get('file_name', 'unknown') for r in low_confidence)}")
        
        # Play sound if configured (Mac only)
        if config.get('play_sound', False) and sys.platform == 'darwin':
            os.system('afplay /System/Library/Sounds/Glass.aiff')
    else:
        print("\n✗ No receipts were successfully processed")
        sys.exit(1)


if __name__ == '__main__':
    main()
