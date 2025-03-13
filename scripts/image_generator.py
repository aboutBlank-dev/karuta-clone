import argparse
import hashlib
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

import cv2
import numpy as np
from schemas.pokemon_card_schema import PokemonTCGCardLoader
from noise import pnoise2

def main():
    parser = argparse.ArgumentParser(
        description="Apply a 'damaged' effect to a card image, filling holes with gray. "
                    "Intensity 0.00 = no damage, 1.00 = maximum damage."
    )
    
    parser.add_argument("pokemon_tcg_id", type=str, 
                        help="Id of the Pokemon TCG Card")
    parser.add_argument("pattern_index", type=int, choices=range(500), 
                        help="Pattern index (0-499) that defines the shape/frequency of the damage.")
    parser.add_argument("torn_intensity", type=float,
                        help="Intensity of the damage effect (0.00 - 1.00).")
    
    args = parser.parse_args()
    if not (0.0 <= args.torn_intensity <= 1.0):
        parser.error("torn_intensity must be between 0.00 and 1.00")
    
    # Load the card and convert to RGBA
    card = PokemonTCGCardLoader.load_id(args.pokemon_tcg_id)
    if not card:
        parser.error("no card matching provided id")

    pil_image = card.get_view().create_image().convert("RGBA")
    # Convert PIL image to OpenCV BGRA format
    image = np.array(pil_image)
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
        
    torn_edges(image, card.id, "damaged_card.png", args.pattern_index, args.torn_intensity)

def generate_seed(card_id, pattern_index):
    """
    Generates a unique seed based on card_id and pattern_index.
    """
    seed_input = f"{card_id}_{pattern_index}"
    seed = int(hashlib.md5(seed_input.encode()).hexdigest(), 16)
    return seed & 0x7FFFFFFF  # Limit to a 31-bit integer

def generate_noise_pattern(width, height, card_id, pattern_index, scale=10.0):
    """
    Generate a structured Perlin noise pattern for consistent tearing effects.
    The output is already in the range [0..255].
    """
    seed = generate_seed(card_id, pattern_index)
    offset_x = seed % 1000
    offset_y = (seed // 1000) % 1000

    noise_pattern = np.zeros((height, width), dtype=np.float32)
    for y in range(height):
        for x in range(width):
            noise_pattern[y, x] = pnoise2(
                (x + offset_x) / scale,
                (y + offset_y) / scale,
                octaves=4
            )
    # Scale the noise to [0..255]
    noise_pattern = ((noise_pattern - noise_pattern.min()) /
                     (noise_pattern.max() - noise_pattern.min())) * 255
    return noise_pattern.astype(np.uint8)

def torn_edges(image, card_id, output_path, pattern_index, torn_intensity):
    """
    Apply a 'damaged' effect to an image, replacing 'holes' with gray.
    
    - pattern_index: controls the shape/frequency of holes via Perlin noise.
    - torn_intensity: 
        0.0 -> minimal grey coverage (nearly no damage).
        1.0 -> maximum grey coverage (heavily damaged).
    """

    if pattern_index < 0 or pattern_index > 499:
        raise Exception("pattern_index must be between 0-499")

    height, width = image.shape[:2]

    # If intensity is 0, write the original image unchanged.
    if torn_intensity == 0:
        cv2.imwrite(output_path, image)
        return

    # Generate structured Perlin noise in [0..255].
    scale = 30.0 + pattern_index  # Slightly vary the noise scale
    noise_pattern = generate_noise_pattern(width, height, card_id, pattern_index, scale=scale)

    # Blur the noise for smoother transitions.
    blur_kernel = int(15 + torn_intensity * 50)
    if blur_kernel % 2 == 0:
        blur_kernel += 1
    mask = cv2.GaussianBlur(noise_pattern, (blur_kernel, blur_kernel), 0)

    # We define a threshold that increases with torn_intensity:
    #  - At intensity=0 -> threshold ~ 50 => almost everything above 50 is kept => minimal grey
    #  - At intensity=1 -> threshold ~ 200 => only very high noise is kept => big grey coverage
    threshold_value = int(50 + 150 * torn_intensity)

    # Standard binary threshold:
    #   if pixel > threshold => 255 => keep card
    #   else => 0 => hole => replaced with gray
    _, mask = cv2.threshold(mask, threshold_value, 255, cv2.THRESH_BINARY)

    # Define the hole color (B, G, R, A). Adjust as needed.
    gray_color = np.array([128, 128, 128, 255], dtype=np.uint8)

    # Where mask == 0, replace the pixel with gray_color.
    hole_indices = (mask == 0)
    image[hole_indices] = gray_color

    # Keep the alpha channel fully opaque.
    image[:, :, 3] = 255

    # Save the final image
    cv2.imwrite(output_path, image)

if __name__ == '__main__':
    main()
