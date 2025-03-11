import random

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
        try:
            if self.is_shiny:
                return self.pokemon["images"]["front_shiny"]
            else:
                return self.pokemon["images"]["front_default"]
        except KeyError:
            # Write into a file the key that is missing
            # Create a file if it does not exist
            with open("missing_keys.txt", "a") as f:
                f.write(f"{self.pokemon['name']} - {self.is_shiny}\n")

            return None
