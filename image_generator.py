from PIL import Image, ImageDraw
import io
from card import Card  # Import the Card class

def create_image(cards: list[Card]) -> io.BytesIO:
    """Generates an image with the given list of Card objects."""
    width, height = 600, 300
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(img)

    ## calculate the card positions based on the number of cards
    card_positions = [(50 + i * 170, 50) for i in range(len(cards))]

    # Draw each card by calling its draw method
    for i, card in enumerate(cards):
        card.draw(draw, card_positions[i])

    # Save the image to a BytesIO object
    byte_io = io.BytesIO()
    img.save(byte_io, 'PNG')  # Save as PNG with transparency
    byte_io.seek(0)

    return byte_io


cards = [
    Card("Card 1", "red"),
    Card("Card 2", "green"),
    Card("Card 3", "blue")
]
bytes = create_image(cards)

with open('image.png', 'wb') as file:
    file.write(bytes.read())

