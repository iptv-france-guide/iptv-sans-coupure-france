import os
from PIL import Image, ImageDraw, ImageFont

def create_pinterest_pin(title, subtitle, background_path, output_path):
    """
    Generates a Pinterest-optimized pin (1000x1500) from a background image.
    """
    width = 1000
    height = 1500
    
    # 1. Open and resize background
    try:
        bg = Image.open(background_path).convert("RGBA")
    except Exception as e:
        print(f"Error loading background: {e}")
        # Create a solid color fallback if no background image is available
        bg = Image.new("RGBA", (width, height), "#0f4c81")
        
    # Calculate aspect ratio to cover the 1000x1500 canvas
    bg_ratio = bg.width / bg.height
    target_ratio = width / height
    
    if bg_ratio > target_ratio:
        # Background is wider than needed, crop horizontally
        new_width = int(height * bg_ratio)
        bg = bg.resize((new_width, height), Image.LANCZOS)
        left = (new_width - width) // 2
        bg = bg.crop((left, 0, left + width, height))
    else:
        # Background is taller than needed, crop vertically
        new_height = int(width / bg_ratio)
        bg = bg.resize((width, new_height), Image.LANCZOS)
        top = (new_height - height) // 2
        bg = bg.crop((0, top, width, top + height))

    # 2. Add a dark gradient overlay for text readability
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Create gradient from top (dark) to bottom (darker)
    for y in range(height):
        # Alpha goes from 120 (top) to 200 (bottom)
        alpha = int(120 + (100 * (y / height)))
        draw.line([(0, y), (width, y)], fill=(10, 53, 97, alpha))
        
    bg = Image.alpha_composite(bg, overlay)
    draw = ImageDraw.Draw(bg)

    # 3. Load Fonts (using default if custom not found)
    try:
        # Try to use system fonts if available
        title_font = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 72)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 40)
        badge_font = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 32)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()

    # 4. Draw elements
    # Add a top badge
    badge_text = "Guide 2026"
    badge_width = 200
    badge_height = 50
    badge_x = (width - badge_width) // 2
    badge_y = 150
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_width, badge_y + badge_height], 
                           radius=25, fill="#f97316")
    
    # Very basic text centering since getsize is deprecated in newer PIL
    draw.text((width//2, badge_y + 8), badge_text, font=badge_font, fill="white", anchor="mt")

    # Draw Title (handling multi-line)
    margin = 80
    current_h = 250
    
    words = title.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        # Rough estimation for word wrap
        if len(" ".join(current_line)) > 20:
            lines.append(" ".join(current_line[:-1]))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
        
    for line in lines:
        draw.text((width//2, current_h), line, font=title_font, fill="white", anchor="mt", align="center")
        current_h += 90

    # Draw Subtitle
    current_h += 40
    draw.text((width//2, current_h), subtitle, font=subtitle_font, fill="#e2e8f0", anchor="mt", align="center")

    # Add URL at the bottom
    draw.text((width//2, height - 100), "IPTVGuide.fr", font=subtitle_font, fill="#f97316", anchor="mt")

    # 5. Save the image
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    bg.convert("RGB").save(output_path, "JPEG", quality=90)
    print(f"✅ Generated Pin: {output_path}")

if __name__ == "__main__":
    # Ensure Pillow is installed: pip install Pillow
    
    # Background image (use your hero banner)
    bg_image = "hero-banner.png"
    
    # List of pins to generate
    pins_data = [
        {
            "title": "Les 5 Meilleurs IPTV\nSans Coupure en France",
            "subtitle": "Classement officiel 2026 testé sur 30 jours",
            "filename": "pins/pin_top_5_iptv.jpg"
        },
        {
            "title": "AuraPlay TV Avis 2026 :\nLe N°1 en France ?",
            "subtitle": "Pourquoi c'est le meilleur choix pour le streaming",
            "filename": "pins/pin_auraplay_avis.jpg"
        },
        {
            "title": "Quel Débit Internet\nPour l'IPTV 4K ?",
            "subtitle": "Guide complet pour éviter les coupures",
            "filename": "pins/pin_debit_4k.jpg"
        },
        {
            "title": "IPTV sur Firestick :\nGuide d'Installation Rapide",
            "subtitle": "Configurez votre Smart TV en 5 minutes",
            "filename": "pins/pin_firestick_install.jpg"
        }
    ]
    
    print("🎨 Generating Pinterest Pins...")
    for pin in pins_data:
        create_pinterest_pin(
            title=pin["title"],
            subtitle=pin["subtitle"],
            background_path=bg_image,
            output_path=pin["filename"]
        )
    print("✨ All pins generated successfully!")
