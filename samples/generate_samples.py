#!/usr/bin/env python3
"""
Generate sample receipt images for testing.
Run this to create sample receipts in the samples/ folder.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_receipt_starbucks():
    """Create a clean Starbucks receipt."""
    # Create image
    img = Image.new('RGB', (400, 500), color='white')
    draw = ImageDraw.Draw(img)
    
    # Use default font (no external font dependency)
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw receipt content
    y = 20
    
    # Header
    draw.text((200, y), "STARBUCKS", fill='black', font=font_large, anchor="mm")
    y += 30
    draw.text((200, y), "Singapore", fill='black', font=font_small, anchor="mm")
    y += 20
    draw.text((200, y), "123 Orchard Road", fill='black', font=font_small, anchor="mm")
    y += 15
    draw.text((200, y), "Tel: +65 6123 4567", fill='black', font=font_small, anchor="mm")
    y += 30
    
    # Line
    draw.line([(20, y), (380, y)], fill='black', width=1)
    y += 15
    
    # Date
    draw.text((20, y), "Date: 18/02/2025", fill='black', font=font_small)
    y += 20
    draw.text((20, y), "Time: 09:45 AM", fill='black', font=font_small)
    y += 20
    draw.text((20, y), "Receipt: #SB250218001", fill='black', font=font_small)
    y += 25
    
    # Line
    draw.line([(20, y), (380, y)], fill='black', width=1)
    y += 15
    
    # Items
    draw.text((20, y), "1x Venti Latte", fill='black', font=font_medium)
    draw.text((380, y), "$6.50", fill='black', font=font_medium, anchor="rm")
    y += 25
    
    draw.text((20, y), "1x Butter Croissant", fill='black', font=font_medium)
    draw.text((380, y), "$4.20", fill='black', font=font_medium, anchor="rm")
    y += 25
    
    draw.text((20, y), "1x Iced Americanano", fill='black', font=font_medium)
    draw.text((380, y), "$5.80", fill='black', font=font_medium, anchor="rm")
    y += 30
    
    # Line
    draw.line([(20, y), (380, y)], fill='black', width=1)
    y += 15
    
    # Totals
    draw.text((20, y), "Subtotal:", fill='black', font=font_small)
    draw.text((380, y), "$16.50", fill='black', font=font_small, anchor="rm")
    y += 20
    
    draw.text((20, y), "GST (9%):", fill='black', font=font_small)
    draw.text((380, y), "$1.49", fill='black', font=font_small, anchor="rm")
    y += 25
    
    draw.text((20, y), "TOTAL:", fill='black', font=font_medium)
    draw.text((380, y), "$17.99", fill='black', font=font_medium, anchor="rm")
    y += 30
    
    # Line
    draw.line([(20, y), (380, y)], fill='black', width=1)
    y += 15
    
    # Payment
    draw.text((20, y), "Payment: Visa ****1234", fill='black', font=font_small)
    y += 20
    draw.text((20, y), "Thank you!", fill='black', font=font_medium)
    
    return img


def create_receipt_ntuc():
    """Create an NTUC FairPrice receipt."""
    img = Image.new('RGB', (400, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    y = 20
    
    # Header
    draw.text((200, y), "NTUC FAIRPRICE", fill='black', font=font_large, anchor="mm")
    y += 30
    draw.text((200, y), "Tampines Mall", fill='black', font=font_small, anchor="mm")
    y += 15
    draw.text((200, y), "GST Reg: M90321345X", fill='black', font=font_small, anchor="mm")
    y += 30
    
    # Line
    draw.line([(20, y), (380, y)], fill='black', width=1)
    y += 15
    
    # Date
    draw.text((20, y), "Date: 17/02/2025  14:32", fill='black', font=font_small)
    y += 20
    draw.text((20, y), "Receipt: FP1702250892", fill='black', font=font_small)
    y += 25
    
    # Line
    draw.line([(20, y), (380, y)], fill='black', width=1)
    y += 15
    
    # Items
    items = [
        ("Fresh Milk 2L", "$5.45"),
        ("Gardenia Bread", "$2.85"),
        ("Eggs (10pcs)", "$3.20"),
        ("Bananas (1kg)", "$2.10"),
        ("Rice 5kg", "$12.50"),
        ("Cooking Oil 1L", "$4.80"),
        ("Toilet Paper 10s", "$6.90"),
    ]
    
    for item, price in items:
        draw.text((20, y), item, fill='black', font=font_medium)
        draw.text((380, y), price, fill='black', font=font_medium, anchor="rm")
        y += 22
    
    y += 10
    
    # Line
    draw.line([(20, y), (380, y)], fill='black', width=1)
    y += 15
    
    # Totals
    draw.text((20, y), "Subtotal:", fill='black', font=font_small)
    draw.text((380, y), "$37.80", fill='black', font=font_small, anchor="rm")
    y += 20
    
    draw.text((20, y), "GST (9%):", fill='black', font=font_small)
    draw.text((380, y), "$2.62", fill='black', font=font_small, anchor="rm")
    y += 25
    
    draw.text((20, y), "TOTAL:", fill='black', font=font_medium)
    draw.text((380, y), "$40.42", fill='black', font=font_medium, anchor="rm")
    y += 30
    
    # Line
    draw.line([(20, y), (380, y)], fill='black', width=1)
    y += 15
    
    # Payment
    draw.text((20, y), "Payment: PayLah!", fill='black', font=font_small)
    y += 20
    draw.text((20, y), "You saved: $2.50", fill='black', font=font_small)
    y += 25
    draw.text((200, y), "Thank you for shopping!", fill='black', font=font_small, anchor="mm")
    
    return img


def create_receipt_grab():
    """Create a Grab ride receipt."""
    img = Image.new('RGB', (400, 450), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    y = 20
    
    # Header
    draw.text((200, y), "GRAB", fill='green', font=font_large, anchor="mm")
    y += 30
    draw.text((200, y), "E-Receipt", fill='black', font=font_medium, anchor="mm")
    y += 30
    
    # Line
    draw.line([(20, y), (380, y)], fill='black', width=1)
    y += 15
    
    # Trip details
    draw.text((20, y), "Date: 16/02/2025", fill='black', font=font_small)
    y += 20
    draw.text((20, y), "Time: 18:45 - 19:12", fill='black', font=font_small)
    y += 20
    draw.text((20, y), "Trip ID: GRB-250216-8842", fill='black', font=font_small)
    y += 25
    
    # Route
    draw.text((20, y), "From:", fill='black', font=font_small)
    y += 15
    draw.text((40, y), "Raffles Place", fill='black', font=font_medium)
    y += 25
    
    draw.text((20, y), "To:", fill='black', font=font_small)
    y += 15
    draw.text((40, y), "Tampines Street 21", fill='black', font=font_medium)
    y += 30
    
    # Line
    draw.line([(20, y), (380, y)], fill='black', width=1)
    y += 15
    
    # Fare breakdown
    draw.text((20, y), "Fare Breakdown:", fill='black', font=font_medium)
    y += 25
    
    draw.text((20, y), "Base Fare", fill='black', font=font_small)
    draw.text((380, y), "$3.00", fill='black', font=font_small, anchor="rm")
    y += 20
    
    draw.text((20, y), "Distance (12.5km)", fill='black', font=font_small)
    draw.text((380, y), "$8.50", fill='black', font=font_small, anchor="rm")
    y += 20
    
    draw.text((20, y), "Time (27 min)", fill='black', font=font_small)
    draw.text((380, y), "$3.20", fill='black', font=font_small, anchor="rm")
    y += 20
    
    draw.text((20, y), "Peak Hour Surcharge", fill='black', font=font_small)
    draw.text((380, y), "$2.00", fill='black', font=font_small, anchor="rm")
    y += 25
    
    # Line
    draw.line([(20, y), (380, y)], fill='black', width=1)
    y += 15
    
    # Total
    draw.text((20, y), "TOTAL:", fill='black', font=font_medium)
    draw.text((380, y), "$16.70", fill='black', font=font_medium, anchor="rm")
    y += 20
    
    draw.text((20, y), "(GST not applicable for transport)", fill='gray', font=font_small)
    y += 30
    
    # Line
    draw.line([(20, y), (380, y)], fill='black', width=1)
    y += 15
    
    # Payment
    draw.text((20, y), "Payment: GrabPay", fill='black', font=font_small)
    y += 20
    draw.text((200, y), "Thank you for riding with Grab!", fill='black', font=font_small, anchor="mm")
    
    return img


def main():
    """Generate all sample receipts."""
    samples_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Generating sample receipts...")
    
    # Create receipts
    receipts = {
        'receipt-starbucks.jpg': create_receipt_starbucks(),
        'receipt-ntuc.jpg': create_receipt_ntuc(),
        'receipt-grab.jpg': create_receipt_grab(),
    }
    
    # Save images
    for filename, img in receipts.items():
        filepath = os.path.join(samples_dir, filename)
        img.save(filepath, 'JPEG', quality=95)
        print(f"  ✓ Created {filename}")
    
    print(f"\nDone! Created {len(receipts)} sample receipts in {samples_dir}/")
    print("\nYou can now test the expense parser with:")
    print("  python parse_receipt.py samples/receipt-starbucks.jpg --verbose")


if __name__ == '__main__':
    main()
