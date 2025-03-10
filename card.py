from PIL import ImageDraw

class Card:
    CARD_WIDTH = 150
    CARD_HEIGHT = 200

    def __init__(self, title, color):
        self.title = title
        self.color = color

    def draw(self, draw: ImageDraw.ImageDraw, position: tuple[int,int]):
        """Draws the card on the provided ImageDraw object at the given position."""

        # Draw the card's rectangle
        draw.rectangle([position, (position[0] + self.CARD_WIDTH, position[1] + self.CARD_HEIGHT)], outline='black', width=2, fill=self.color)

        # Calculate the size of the text to center it
        text_bbox = draw.textbbox((position[0], position[1]), self.title)
        text_width = text_bbox[2] - text_bbox[0]  # Right - Left
        text_height = text_bbox[3] - text_bbox[1]  # Bottom - Top

        # Calculate the position to center the text
        text_x = position[0] + (self.CARD_WIDTH - text_width) // 2  # Horizontal centering
        text_y = position[1] + (self.CARD_HEIGHT - text_height) // 2  # Vertical centering

        # Draw the card's title text at the calculated position
        draw.text((text_x, text_y), self.title, fill='black')

