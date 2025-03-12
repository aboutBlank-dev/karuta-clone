from pathlib import Path
from pydantic import BaseModel
from scripts.pokemon_tcg_saver import load_pokemon_tcg_card_data, load_pokemon_tcg_card_image
from utils.file_utils import get_random_subdirectory

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
    def load_id(id) -> PokemonCardSchema:
        return load_pokemon_tcg_card_data(id)
    
    def random() -> PokemonCardSchema:
        PROJECT_ROOT = Path(__file__).resolve().parent.parent
        data_dir = PROJECT_ROOT / "pokemon_tcg_data"
        id = get_random_subdirectory(data_dir)
        return load_pokemon_tcg_card_data(id)
