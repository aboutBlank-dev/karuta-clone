from io import BytesIO
import random
import pokebase as pb
import requests
from PIL import Image

from pokemon_saver import load_pokemon_data

MAX_POKEMON_ID = 1025
SHINY_CHANCE = 1/4096

class Pokemon:
    def __init__(self, id=None):
        if id is None:
            id = random.randint(1, MAX_POKEMON_ID)

        self.pokemon = load_pokemon_data(id)
        self.is_shiny = random.random() < SHINY_CHANCE
    
    def get_name(self) -> str:
        return self.pokemon.name

    def get_sprite(self):
        if self.is_shiny:
            return self.pokemon["images"]["front_shiny"]
        else:
            return self.pokemon["images"]["front_default"]
