from PIL import Image, ImageDraw
import io
from card import Card
from pokemon import Pokemon  # Import the Card class

def create_drop_image(cards: list[Card], spacing: int = 10, padding: int = 20) -> io.BytesIO:
    # Calculate combined width and height including spacing and padding
    combined_width = (Card.CARD_WIDTH * len(cards)) + (spacing * (len(cards) - 1)) + (2 * padding)
    combined_height = Card.CARD_HEIGHT + (2 * padding)

    # Create a new image with the specified width and height
    combined_image = Image.new("RGBA", (combined_width, combined_height), (0, 0, 0, 0))  # Transparent background

    # Place the cards on the combined image with spacing
    for i, card in enumerate(cards):
        card_image = card.create_image()  # This function creates an image for each card (implement it based on your logic)
        alpha_channel = card_image.split()[3]  # Get the alpha channel (the 4th channel)

        # Calculate the position considering padding and spacing between cards
        x_position = padding + i * (Card.CARD_WIDTH + spacing)
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
    cards = [Card(Pokemon()) for _ in range(3)]

    # Generate the drop image
    image = create_drop_image(cards)

    # Save the image to a file
    with open('drop_image.png', 'wb') as f:
        f.write(image.getvalue())


if __name__ == '__main__':
    main()

