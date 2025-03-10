from PIL import ImageDraw, Image
from pokemon import Pokemon

class Card:
    CARD_WIDTH = 150
    CARD_HEIGHT = 200

    def __init__(self, pokemon: Pokemon, color: str):
        self.color = color
        self.pokemon = pokemon


    def draw(self, draw: ImageDraw.ImageDraw, img: Image, position: tuple[int,int]):
        """Draws the card on the provided ImageDraw object at the given position."""
        # Draw the card's rectangle
        draw.rectangle([position, (position[0] + self.CARD_WIDTH, position[1] + self.CARD_HEIGHT)], outline='black', width=2, fill=self.color)

        sprite_img = self.pokemon.get_sprite()
        
        # Resize the sprite image to fit within the card
        sprite_img = sprite_img.resize((150, 150))  # You can adjust the size as needed
        
        # Calculate position to center the sprite image on the card
        sprite_x = position[0] + (self.CARD_WIDTH - sprite_img.width) // 2
        sprite_y = position[1] + (self.CARD_HEIGHT - sprite_img.height) // 2  # Slight offset to avoid overlap with title
        
        # Paste the sprite onto the card
        img.paste(sprite_img, (sprite_x, sprite_y), sprite_img)


