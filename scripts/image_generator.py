import argparse
import hashlib
import os
import random
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from schemas.pokemon_card_schema import PokemonTCGCardLoader
from PIL import Image

def generate_seed(card_id, pattern_number):
    """
    Generates a unique seed based on card_id and pattern_number.
    """
    seed_input = f"{card_id}_{pattern_number}"
    seed = int(hashlib.md5(seed_input.encode()).hexdigest(), 16)
    return seed & 0x7FFFFFFF  # Limit to a 31-bit integer


def apply_pattern_damage(image, seed, float_value, scratch_colour=[255, 194, 133]):
    """Applies a random portion of scratch.png as damage."""

    try:
        scratch_image = Image.open("scratch.png").convert("RGBA")
    except FileNotFoundError:
        print("Error: scratch.png not found!")
        return image

    card_width, card_height = image.size
    scratch_width, scratch_height = scratch_image.size

    random.seed(seed)  # Seed the random number generator

    # Random cropping with variable scale
    scale_factor = random.uniform(0.8, 1.2)  # Scale between 80% and 120% of card size
    scaled_width = int(card_width * scale_factor)
    scaled_height = int(card_height * scale_factor)

    # Ensure the scaled crop stays within the image bounds
    max_x = scratch_width - scaled_width
    max_y = scratch_height - scaled_height

    if max_x < 0:
        scaled_width = scratch_width
        max_x = 0
    if max_y < 0:
        scaled_height = scratch_height
        max_y = 0

    start_x = random.randint(0, max_x)
    start_y = random.randint(0, max_y)

    cropped_scratch = scratch_image.crop((start_x, start_y, start_x + scaled_width, start_y + scaled_height))

    # Resize to the original card dimensions
    cropped_scratch = cropped_scratch.resize((card_width, card_height), Image.Resampling.LANCZOS)

    # Random transformations (flips)
    flip_x = random.choice([True, False])
    flip_y = random.choice([True, False])

    if flip_x:
        cropped_scratch = cropped_scratch.transpose(Image.FLIP_LEFT_RIGHT)
    if flip_y:
        cropped_scratch = cropped_scratch.transpose(Image.FLIP_TOP_BOTTOM)
        
    # Change the color of the scratches.
    r, g, b, a = cropped_scratch.split()
    new_r = r.point(lambda i: scratch_colour[0] if i > 0 else 0)
    new_g = g.point(lambda i: scratch_colour[1] if i > 0 else 0)
    new_b = b.point(lambda i: scratch_colour[2] if i > 0 else 0)
    cropped_scratch = Image.merge("RGBA", (new_r, new_g, new_b, a))

    # Modify the alpha channel based on the fade value.
    alpha = cropped_scratch.split()[3]  # Get the alpha channel
    alpha = alpha.point(lambda i: int(i * float_value))  # Scale alpha values

    # Create a new image with the modified alpha.
    cropped_scratch.putalpha(alpha)

    # Apply the cropped scratch as an alpha mask.
    image.paste(cropped_scratch, (0, 0), cropped_scratch)

    return image


def main():
    parser = argparse.ArgumentParser(
        description="Apply a 'damaged' effect to a card image, filling holes with gray. "
                    "Intensity 0.00 = no damage, 1.00 = maximum damage."
    )
    
    parser.add_argument("pokemon_tcg_id", type=str, 
                        help="Id of the Pokemon TCG Card")
    parser.add_argument("pattern_number", type=int, choices=range(500), 
                        help="Pattern number (0-499) that defines the shape/frequency of the damage.")
    parser.add_argument("float_value", type=float,
                        help="Intensity of the damage effect (0.00 - 1.00).")
    
    args = parser.parse_args()
    if not (0.0 <= args.float_value <= 1.0):
        parser.error("torn_intensity must be between 0.00 and 1.00")
    
    # Load the card and convert to RGBA
    card = PokemonTCGCardLoader.load_id(args.pokemon_tcg_id)
    if not card:
        parser.error("no card matching provided id")

    pil_image = card.get_view().create_image().convert("RGBA")

    # Convert PIL image to OpenCV BGRA format
    seed = generate_seed(card.id, args.pattern_number)
    damaged_card = apply_pattern_damage(pil_image, seed, args.float_value)
    damaged_card.save("damaged_card.png")


if __name__ == '__main__':
    main()