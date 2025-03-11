from PIL import ImageDraw, Image, ImageFont
from pokemon import Pokemon

class Card:
    CARD_WIDTH = 150
    CARD_HEIGHT = 200

    def __init__(self, pokemon: Pokemon):
        self.pokemon = pokemon


    def draw(self, draw: ImageDraw.ImageDraw, img: Image, position: tuple[int,int]):
        """Draws the card on the provided ImageDraw object at the given position."""
        self._draw_background(draw, img, position)
        self._draw_sprite(draw, img, position)
        self._draw_text(draw, img, position)

        # Draw the frame last to ensure it's on top of the other elements
        self._draw_frame(draw, img, position)
        
    
    def _draw_background(self, draw, img, position):
        draw.rectangle([position, (position[0] + self.CARD_WIDTH, position[1] + self.CARD_HEIGHT)], outline='black', width=2, fill="white")
    
    def _draw_sprite(self, draw, img, position):
        sprite_img = self.pokemon.get_sprite()
        # Resize the sprite image to fit within the card
        sprite_img = sprite_img.resize((128, 128))  # You can adjust the size as needed
        
        # Calculate position to center the sprite image on the card
        sprite_x = position[0] + (self.CARD_WIDTH - sprite_img.width) // 2
        sprite_y = position[1] + (self.CARD_HEIGHT - sprite_img.height) // 2  # Slight offset to avoid overlap with title
        sprite_y -= 25  # Move the sprite up slightly
        
        # Paste the sprite onto the card
        img.paste(sprite_img, (sprite_x, sprite_y), sprite_img)
    
    def _draw_frame(self, draw, img, position):
        frame_img = Image.open("card_frame.png")
        img.paste(frame_img, position, frame_img)

    def _draw_text(self, draw, img, position):
        # Load the default font
        font_path = "minecraft-font.ttf"  # Adjust based on your system
        font_size = 15  # You can change this value to control the font size
        font = ImageFont.truetype(font_path, font_size)

        # Get the centered position for the text
        text_x = position[0] + self.CARD_WIDTH // 2
        image_height = img.size[1]
        text_y = image_height - 83 # Slightly above the bottom of the card

        # Get the bounding box of the text to properly center it
        pokemon_name = self.pokemon.get_formatted_name()
        bbox = draw.textbbox((0, 0), pokemon_name, font=font)  # Get the bounding box of the text
        text_width = bbox[2] - bbox[0]  # Width of the text (bbox[2] is the rightmost x-coordinate, bbox[0] is the leftmost)

        # Adjust text_x to center the text
        text_x -= text_width // 2  # Centering the text horizontally

        # Add the Pokémon name to the card using the default font
        draw.text((text_x, text_y), pokemon_name, fill='black', font=font)
