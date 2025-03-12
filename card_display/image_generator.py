from PIL import Image, ImageDraw
import io
from card_display.abstract_card_display import AbstractCardDisplay
from card_display.pokemon_card_display import PokemonCardDisplay
from schemas.pokemon_schema import PokemonSchema
from schemas.pokemon_card_schema import PokemonCardSchema, PokemonTCGCardLoader
from card_display.pokemon_tcg_card_display import PokemonTCGCardDisplay  # Import the Card class

def create_drop_image(cards: list[AbstractCardDisplay], spacing: int = 20, padding: int = 20) -> io.BytesIO:
    # Calculate combined width and height including spacing and padding
    # We generate first card ahead of time since we need to update the width/height (which we get from the loaded image)
    first_card = cards[0]
    first_card_image = first_card.create_image()

    combined_width = (first_card.CARD_WIDTH * len(cards)) + (spacing * (len(cards) - 1)) + (2 * padding)
    combined_height = first_card.CARD_HEIGHT + (2 * padding)

    # Create a new image with the specified width and height
    combined_image = Image.new("RGBA", (combined_width, combined_height), (0, 0, 0, 0))  # Transparent background

    # Place the cards on the combined image with spacing
    for i, card in enumerate(cards):
        card_image = first_card_image if (i == 0) else card.create_image()  
        alpha_channel = card_image.split()[3]  # Get the alpha channel (the 4th channel)

        # Calculate the position considering padding and spacing between cards
        x_position = padding + i * (card.CARD_WIDTH + spacing)
        y_position = padding

        # Paste the card image onto the combined image with its alpha channel as a mask
        combined_image.paste(card_image, (x_position, y_position), alpha_channel)

    # Save the image to a BytesIO object
    byte_io = io.BytesIO()
    combined_image.save(byte_io, 'PNG')  # Save as PNG with transparency
    byte_io.seek(0)

    return byte_io

def main():
    # Create a list of Card objects
    # cards = [PokemonCardView(Pokemon()) for _ in range(3)]
    cards = [PokemonTCGCardLoader.random().get_view() for _ in range(3)]

    # Generate the drop image
    image = create_drop_image(cards)
    print(f"Generated card ids: {cards[0].card.id} , {cards[1].card.id}, {cards[2].card.id}")

    # Save the image to a file
    with open('drop_image.png', 'wb') as f:
        f.write(image.getvalue())


if __name__ == '__main__':
    main()

