"""
Script to generate a crisp college logo emblem for the Smart Campus Helpdesk application.
Uses Pillow to draw geometric shapes and academic symbols.
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_college_logo():
    # 256x256 high-resolution icon
    size = (256, 256)
    img = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    c_dark_green = (23, 61, 45, 255)    # #173D2D
    c_primary = (35, 134, 83, 255)      # #238653
    c_gold = (233, 162, 59, 255)        # #E9A23B
    c_white = (255, 255, 255, 255)
    c_light_green = (244, 247, 245, 255)

    # Draw Outer Shield / Circle with subtle border
    # Outer circle border
    draw.ellipse([8, 8, 248, 248], fill=c_dark_green, outline=c_gold, width=4)
    # Inner ring
    draw.ellipse([20, 20, 236, 236], fill=c_primary, outline=c_white, width=2)

    # Campus Building / Classical Pillars Motif in the center
    # Pediment (triangle roof)
    roof_coords = [(128, 55), (75, 95), (181, 95)]
    draw.polygon(roof_coords, fill=c_white)
    # Inner roof triangle
    draw.polygon([(128, 68), (88, 92), (168, 92)], fill=c_primary)

    # Architrave beam
    draw.rectangle([72, 95, 184, 103], fill=c_white)

    # 4 Classical Pillars
    pillars = [(82, 103, 94, 150), (106, 103, 118, 150), (138, 103, 150, 150), (162, 103, 174, 150)]
    for p in pillars:
        draw.rectangle(p, fill=c_white)

    # Base steps
    draw.rectangle([70, 150, 186, 158], fill=c_white)
    draw.rectangle([64, 158, 192, 166], fill=c_gold)

    # Open book below or checkmark shield
    # Open book shape
    # Left page
    draw.polygon([(85, 175), (124, 180), (124, 205), (85, 200)], fill=c_white, outline=c_dark_green, width=1)
    # Right page
    draw.polygon([(171, 175), (132, 180), (132, 205), (171, 200)], fill=c_white, outline=c_dark_green, width=1)
    # Spine center
    draw.line([(128, 180), (128, 205)], fill=c_gold, width=2)

    # Stars on sides
    # Left star dot
    draw.ellipse([45, 122, 55, 132], fill=c_gold)
    # Right star dot
    draw.ellipse([201, 122, 211, 132], fill=c_gold)

    # Save 256x256
    assets_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(assets_dir, "logo.png")
    img.save(logo_path, format="PNG")
    print(f"Generated logo at {logo_path}")

    # Also save 64x64 icon
    small_img = img.resize((64, 64), Image.Resampling.LANCZOS)
    small_path = os.path.join(assets_dir, "logo_small.png")
    small_img.save(small_path, format="PNG")
    print(f"Generated small logo at {small_path}")

if __name__ == "__main__":
    create_college_logo()
