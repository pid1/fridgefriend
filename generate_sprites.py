#!/usr/bin/env python3
"""
Generate placeholder chibi dinosaur sprites for FridgeFriend.
Run this on your computer (not CircuitPython) to create BMP files.

"""

from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Please install Pillow")
    exit(1)

# Output directory
SPRITES_DIR = Path(__file__).parent / "sprites"

# 4-color grayscale palette for e-ink
WHITE = (255, 255, 255)
LIGHT_GRAY = (170, 170, 170)
DARK_GRAY = (85, 85, 85)
BLACK = (0, 0, 0)

# Sprite size
SIZE = 64


def create_base_dino(draw, offset_y=0, eye_style="normal"):
    """Draw a chibi dinosaur base shape."""
    # Body (oval)
    body_left = 16
    body_top = 28 + offset_y
    body_right = 48
    body_bottom = 54 + offset_y
    draw.ellipse([body_left, body_top, body_right, body_bottom], fill=DARK_GRAY, outline=BLACK)

    # Head (circle, overlapping body)
    head_cx, head_cy = 32, 24 + offset_y
    head_r = 14
    draw.ellipse(
        [head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r],
        fill=DARK_GRAY,
        outline=BLACK
    )

    # Belly (lighter oval)
    belly_left = 22
    belly_top = 34 + offset_y
    belly_right = 42
    belly_bottom = 50 + offset_y
    draw.ellipse([belly_left, belly_top, belly_right, belly_bottom], fill=LIGHT_GRAY)

    # Spikes on back
    spike_points = [
        [(20, 20 + offset_y), (24, 12 + offset_y), (28, 20 + offset_y)],
        [(28, 18 + offset_y), (32, 8 + offset_y), (36, 18 + offset_y)],
        [(36, 20 + offset_y), (40, 12 + offset_y), (44, 20 + offset_y)],
    ]
    for points in spike_points:
        draw.polygon(points, fill=LIGHT_GRAY, outline=BLACK)

    # Tail
    tail_points = [(16, 44 + offset_y), (4, 48 + offset_y), (8, 40 + offset_y)]
    draw.polygon(tail_points, fill=DARK_GRAY, outline=BLACK)

    # Legs
    draw.ellipse([20, 50 + offset_y, 28, 58 + offset_y], fill=DARK_GRAY, outline=BLACK)
    draw.ellipse([36, 50 + offset_y, 44, 58 + offset_y], fill=DARK_GRAY, outline=BLACK)

    # Arms
    draw.ellipse([12, 34 + offset_y, 20, 42 + offset_y], fill=DARK_GRAY, outline=BLACK)
    draw.ellipse([44, 34 + offset_y, 52, 42 + offset_y], fill=DARK_GRAY, outline=BLACK)

    # Eyes
    if eye_style == "normal":
        # Normal open eyes
        draw.ellipse([24, 20 + offset_y, 30, 28 + offset_y], fill=WHITE, outline=BLACK)
        draw.ellipse([34, 20 + offset_y, 40, 28 + offset_y], fill=WHITE, outline=BLACK)
        # Pupils
        draw.ellipse([26, 22 + offset_y, 29, 26 + offset_y], fill=BLACK)
        draw.ellipse([36, 22 + offset_y, 39, 26 + offset_y], fill=BLACK)
    elif eye_style == "sleepy":
        # Half-closed sleepy eyes
        draw.arc([24, 22 + offset_y, 30, 28 + offset_y], 0, 180, fill=BLACK, width=2)
        draw.arc([34, 22 + offset_y, 40, 28 + offset_y], 0, 180, fill=BLACK, width=2)
    elif eye_style == "closed":
        # Closed happy eyes (^_^)
        draw.arc([24, 20 + offset_y, 30, 28 + offset_y], 200, 340, fill=BLACK, width=2)
        draw.arc([34, 20 + offset_y, 40, 28 + offset_y], 200, 340, fill=BLACK, width=2)
    elif eye_style == "excited":
        # Big excited eyes
        draw.ellipse([23, 18 + offset_y, 31, 28 + offset_y], fill=WHITE, outline=BLACK)
        draw.ellipse([33, 18 + offset_y, 41, 28 + offset_y], fill=WHITE, outline=BLACK)
        # Sparkle pupils
        draw.ellipse([25, 20 + offset_y, 29, 25 + offset_y], fill=BLACK)
        draw.ellipse([35, 20 + offset_y, 39, 25 + offset_y], fill=BLACK)
        draw.ellipse([26, 21 + offset_y, 28, 23 + offset_y], fill=WHITE)
        draw.ellipse([36, 21 + offset_y, 38, 23 + offset_y], fill=WHITE)

    # Mouth
    if eye_style == "excited":
        # Big smile
        draw.arc([26, 28 + offset_y, 38, 36 + offset_y], 0, 180, fill=BLACK, width=2)
    else:
        # Small smile
        draw.arc([28, 30 + offset_y, 36, 36 + offset_y], 0, 180, fill=BLACK, width=1)


def create_idle_day():
    """Create idle day sprite - normal standing."""
    img = Image.new("RGB", (SIZE, SIZE), WHITE)
    draw = ImageDraw.Draw(img)
    create_base_dino(draw, offset_y=0, eye_style="normal")
    return img


def create_idle_night():
    """Create idle night sprite - sleepy."""
    img = Image.new("RGB", (SIZE, SIZE), WHITE)
    draw = ImageDraw.Draw(img)
    create_base_dino(draw, offset_y=0, eye_style="sleepy")
    # Add Zzz
    draw.text((48, 8), "z", fill=BLACK)
    draw.text((52, 4), "Z", fill=DARK_GRAY)
    return img


def create_play():
    """Create play action sprite - jumping excited."""
    img = Image.new("RGB", (SIZE, SIZE), WHITE)
    draw = ImageDraw.Draw(img)
    create_base_dino(draw, offset_y=-6, eye_style="excited")
    # Add action lines
    draw.line([(10, 56), (14, 52)], fill=DARK_GRAY, width=1)
    draw.line([(50, 56), (46, 52)], fill=DARK_GRAY, width=1)
    # Add sparkles
    draw.text((8, 10), "*", fill=BLACK)
    draw.text((52, 14), "*", fill=BLACK)
    return img


def create_pet():
    """Create pet action sprite - happy with hearts."""
    img = Image.new("RGB", (SIZE, SIZE), WHITE)
    draw = ImageDraw.Draw(img)
    create_base_dino(draw, offset_y=0, eye_style="closed")
    # Add hearts
    def draw_heart(x, y, size=6):
        draw.ellipse([x, y, x + size // 2, y + size // 2], fill=DARK_GRAY)
        draw.ellipse([x + size // 2, y, x + size, y + size // 2], fill=DARK_GRAY)
        draw.polygon([(x, y + size // 3), (x + size // 2, y + size), (x + size, y + size // 3)], fill=DARK_GRAY)

    draw_heart(6, 8, 8)
    draw_heart(50, 12, 6)
    draw_heart(4, 30, 5)
    return img


def create_feed():
    """Create feed action sprite - eating/chomping."""
    img = Image.new("RGB", (SIZE, SIZE), WHITE)
    draw = ImageDraw.Draw(img)

    # Draw dino with open mouth
    create_base_dino(draw, offset_y=0, eye_style="closed")

    # Override mouth with open chomp
    draw.ellipse([28, 30, 38, 38], fill=BLACK)

    # Add food item (leaf)
    draw.ellipse([40, 28, 50, 36], fill=LIGHT_GRAY, outline=DARK_GRAY)
    draw.line([(45, 32), (48, 28)], fill=DARK_GRAY, width=1)

    # Add chomp lines
    draw.arc([24, 26, 42, 42], 30, 150, fill=DARK_GRAY, width=1)
    return img


def create_sleep():
    """Create sleep action sprite - curled up sleeping."""
    img = Image.new("RGB", (SIZE, SIZE), WHITE)
    draw = ImageDraw.Draw(img)

    # Curled up body (more horizontal oval)
    draw.ellipse([12, 32, 52, 56], fill=DARK_GRAY, outline=BLACK)

    # Head resting
    draw.ellipse([36, 24, 58, 46], fill=DARK_GRAY, outline=BLACK)

    # Belly
    draw.ellipse([18, 38, 42, 52], fill=LIGHT_GRAY)

    # Closed eyes
    draw.arc([42, 30, 50, 38], 200, 340, fill=BLACK, width=2)

    # Tail curled around
    draw.arc([8, 36, 24, 52], 90, 270, fill=DARK_GRAY, width=4)
    draw.arc([8, 36, 24, 52], 90, 270, fill=BLACK, width=1)

    # Zzz bubbles
    draw.text((54, 16), "z", fill=DARK_GRAY)
    draw.text((58, 10), "Z", fill=BLACK)
    draw.text((60, 4), "Z", fill=DARK_GRAY)

    return img


def convert_to_grayscale_palette(img):
    """Convert image to 4-color grayscale palette for e-ink."""
    # Quantize to 4 colors
    img = img.convert("L")  # Convert to grayscale
    img = img.quantize(colors=4)
    return img.convert("RGB")


def main():
    """Generate all sprite files."""
    SPRITES_DIR.mkdir(exist_ok=True)

    sprites = {
        "idle_day.bmp": create_idle_day,
        "idle_night.bmp": create_idle_night,
        "play.bmp": create_play,
        "pet.bmp": create_pet,
        "feed.bmp": create_feed,
        "sleep.bmp": create_sleep,
    }

    for filename, create_func in sprites.items():
        filepath = SPRITES_DIR / filename
        img = create_func()
        img = convert_to_grayscale_palette(img)
        img.save(filepath, "BMP")
        print(f"Created: {filepath}")

    print(f"\nAll sprites generated in {SPRITES_DIR}")
    print("Copy the 'sprites' folder to your CIRCUITPY drive.")


if __name__ == "__main__":
    main()
