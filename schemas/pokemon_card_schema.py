import os
from pathlib import Path
from pydantic import BaseModel
from scripts.pokemon_tcg_saver import load_pokemon_tcg_card_data
from utils.file_utils import get_random_json_path, get_random_subdirectory

class PokemonCardSchema(BaseModel):
    id: str
    name: str
    number: str
    set: str 
    artist: str | None
    rarity: str | None
    flavor_text: str | None

    def get_view(self):
        from card_display.pokemon_tcg_card_display import PokemonTCGCardDisplay
        return PokemonTCGCardDisplay(self)

class PokemonTCGCardLoader:
    @staticmethod
    def load_id(id) -> PokemonCardSchema:
        return load_pokemon_tcg_card_data(id)
    
    @staticmethod
    def random() -> PokemonCardSchema:
        PROJECT_ROOT = Path(__file__).resolve().parent.parent
        data_dir = os.path.join(PROJECT_ROOT, "pokemon_tcg_data")

        random_set_id = get_random_subdirectory(data_dir)
        set_dir = os.path.join(data_dir, random_set_id)

        random_card_id = get_random_json_path(set_dir, f"{random_set_id}.json")
        return load_pokemon_tcg_card_data(random_card_id)
