import os
from pathlib import Path
from pydantic import BaseModel

from scripts.pokemon_tcg_saver import load_pokemon_tcg_set_data
from utils.file_utils import get_random_subdirectory


class PokemonCardSetSchema(BaseModel):
    id: str
    name: str
    series: str
    printed_total: int
    total: int
    release_date: str

class PokemonCardSetLoader:
    def load_id(id) -> PokemonCardSetSchema:
        return load_pokemon_tcg_set_data(id)
    
    def random() -> PokemonCardSetSchema:
        PROJECT_ROOT = Path(__file__).resolve().parent.parent
        data_dir = os.path.join(PROJECT_ROOT, "pokemon_tcg_data")
        id = get_random_subdirectory(data_dir)
        return load_pokemon_tcg_set_data(id)