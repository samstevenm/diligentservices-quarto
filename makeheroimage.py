# makeheroimage.py
"""
This script generates a hero image with complementary colors and centered text.
It can optionally insert/update the hero image in the .qmd front matter.
requirements: Pillow, PyYAML
"""

import argparse
from PIL import Image, ImageDraw, ImageFont
import random
import os
import sys
import yaml

def generate_complementary_colors():
    # Pantone Orange and complementary colors
    colors = [
        ((255, 165, 0), (0, 0, 255)),  # Orange and Blue
        ((255, 127, 80), (75, 0, 130)),  # Coral and Indigo
        ((255, 69, 0), (0, 128, 128)),  # Red-Orange and Teal
        ((255, 140, 0), (0, 206, 209)),  # Dark Orange and Dark Turquoise
    ]
    return random.choice(colors)

def get_font_path():
    # Check for common font paths in different operating systems
    common_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
        "/System/Library/Fonts/Monaco.ttf",  # macOS
        "C:\\Windows\\Fonts\\Arial.ttf",  # Windows
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    print("Error: Font file not found. Please install DejaVu Sans or Arial font.")
    sys.exit(1)

def create_hero_image(text, output_path="hero_image.png"):
    try:
        # Define image dimensions and background color
        width, height = 1200, 600
        background_color, text_color = generate_complementary_colors()

        # Create an image
        image = Image.new("RGB", (width, height), color=background_color)
        draw = ImageDraw.Draw(image)

        # Define font
        font_path = get_font_path()
        font = ImageFont.truetype(font_path, size=60)

        # Calculate text size and position using textbbox
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        while text_width > width - 140:  # Adjust font size to fit within image width
            font = ImageFont.truetype(font_path, size=font.size - 2)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

        text_x = (width - text_width) / 2
        text_y = (height - text_height) / 2

        # Draw the text on the image
        draw.text((text_x, text_y), text, font=font, fill=text_color)

        # Save the image
        image.save(output_path)
        print(f"Image saved at {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def update_qmd_front_matter(qmd_path, image_path):
    try:
        with open(qmd_path, 'r') as file:
            content = file.read()

        # Find the front matter section
        if content.startswith('---'):
            end_index = content.find('---', 3) + 3
            front_matter = content[3:end_index-3]
            body = content[end_index:]
        else:
            front_matter = ""
            body = content

        # Parse the front matter
        fm_data = yaml.safe_load(front_matter) if front_matter else {}

        # Update the image path to be relative
        fm_data['image'] = os.path.join("images", os.path.basename(image_path))

        # Convert the front matter back to a string
        new_front_matter = yaml.dump(fm_data)

        # Write the updated content back to the file
        with open(qmd_path, 'w') as file:
            file.write(f"---\n{new_front_matter}---\n{body}")

        print(f"Updated {qmd_path} with image {fm_data['image']}")

    except Exception as e:
        print(f"An error occurred while updating the .qmd file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a hero image with specified text.")
    parser.add_argument("text", type=str, help="Text to display on the hero image")
    parser.add_argument("-o", "--output", type=str, default="hero_image.png", help="Output path for the hero image")
    parser.add_argument("-q", "--qmd", type=str, help="Path to the .qmd file to update front matter with the image")
    args = parser.parse_args()

    create_hero_image(args.text, args.output)
    
    if args.qmd:
        update_qmd_front_matter(args.qmd, args.output)
