from pathlib import Path
from scripts.pokemon_tcg_saver import load_pokemon_tcg_card_data
from utils.file_utils import get_random_subdirectory

class PokemonTCGCard:
    def __init__(self, id=None):
        if id is None:
            PROJECT_ROOT = Path(__file__).resolve().parent
            data_dir = PROJECT_ROOT / "pokemon_tcg_data"
            id = get_random_subdirectory(data_dir)
        
        self.pokemon_tcg_card_data = load_pokemon_tcg_card_data(id)
    
    def get_name(self) -> str:
        return self.pokemon_tcg_card_data["name"]

    def get_sprite(self):
        id = self.pokemon_tcg_card_data["id"]
        ##Load image based on id (its in that folder stored as {id}.png)
