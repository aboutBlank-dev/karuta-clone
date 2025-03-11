import argparse
import os
import json
from pathlib import Path
import sys
import requests
from io import BytesIO
from pokemontcgsdk import RestClient
from pokemontcgsdk import Card as TCGCard
from pokemontcgsdk import Set as TCGSet
from PIL import Image
from dotenv import load_dotenv

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.file_utils import sanitize_filename

load_dotenv()
RestClient.configure(os.getenv("POKEMON_TCG_API_KEY"))

# Get the project root (parent of the current script's directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the data directory
data_dir = PROJECT_ROOT / "pokemon_tcg_data"

def save_all_sets(force=False):
    all_sets = TCGSet.all()
    for set in all_sets:
        save_set_data(set, force)

def save_set_data(set: TCGSet, force=False):
    sets_folder = os.path.join(data_dir, "sets")
    if os.path.exists(sets_folder) and not force:
        print(f"Skipping set with ID {set.id} ({set.name}) as it already exists at {sets_folder}")
        return

    os.makedirs(sets_folder, exist_ok=True)

    save_data = {
        "id": set.id,
        "name": set.name,
        "series": set.series,
        "printed_total": set.printedTotal,
        "total": set.total,
        "release_date": set.releaseDate
    }

    with open(os.path.join(sets_folder, f'{set.id}.json'), 'w') as file:
        json.dump(save_data, file, indent=2)
    
    print(f"Saved {set.name} with ID: {set.id} successfully")

def save_all_cards(force=False):
    page = 1
    while True:
        cards = TCGCard.where(page=page, pageSize=100)

        print(f"Will save the next {len(cards)} cards.") 
        for card in cards:
            save_card_data(card, force)

        # If the number of cards returned is less than the page_size, stop.
        if len(cards) < 100:
            print("Finished saving all card data.")
            break
        
        page += 1

def save_card_data(card: TCGCard, force=False):
    card_folder = os.path.join(data_dir, sanitize_filename(card.id))
    if os.path.exists(card_folder) and not force:
        print(f"Skipping Card with ID {card.id} ({card.name}) as it already exists at {card_folder}")
        return
    
    os.makedirs(card_folder, exist_ok=True)

    # Save the images
    _save_card_sprites(card, card_folder)

    save_data = {
        "id": card.id,
        "name": card.name,
        "number": card.number,
        "artist": card.artist,
        "rarity": card.rarity,
        "flavor_text": card.flavorText,
        "set" : card.set.id #sets are stored separately     
    }

    file_name = sanitize_filename(f"{card.id}.json")
    with open(os.path.join(card_folder, file_name), 'w') as file:
        json.dump(save_data, file, indent=2)
    
    print(f"Saved {card.name} with ID: {card.id} successfully")

def _save_card_sprites(card: TCGCard, card_folder: str):
    image_url = card.images.small
    try:
        # Download the sprite image
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception if there's an error

        # Save the image in the appropriate file
        image_name = sanitize_filename(f'{card.id}.png')
        try:
            img = Image.open(BytesIO(response.content))
            img.save(os.path.join(card_folder, image_name))
        except Exception as e:
            print(f"Error saving {card.name} for Card ID {card.id} Image Url: {image_url} Error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {card.name} for Card ID {card.id}: {e}")
    

def main():
    parser = argparse.ArgumentParser(description="Download Pokémon Card data.")
    parser.add_argument("id", type=str, help="Pokemon Card ID or 'all' to fetch all Pokémon.")
    parser.add_argument("--force", action="store_true", help="Force the download of the Pokémon Card data.")
    parser.add_argument("--sets", action="store_true", help="Download all the sets.")

    # Create directories for storing data
    # Ensure the main directory exists
    os.makedirs(data_dir, exist_ok=True)

    args = parser.parse_args()
    if args.sets:
        save_all_sets(args.force)

    if args.id == "all":
        save_all_cards(args.force)  # Fetch and process all Pokémon
    else:
        try:
            card_id = args.id
            card = TCGCard.find(card_id)
            save_card_data(card, args.force)
        except Exception as e:
            print("[ERROR] Invalid Pokémon Card ID. Please provide a valid id or 'all'.")

if __name__ == "__main__":
    main()

def load_pokemon_tcg_card_data(pokemon_tcg_card_id):
    # Load Pokémon data from JSON file
    folder_name = sanitize_filename(pokemon_tcg_card_id)
    file_name = sanitize_filename(f'{pokemon_tcg_card_id}.json')
    card_file = os.path.join(data_dir, folder_name)
    card_file = os.path.join(card_file, file_name)

    with open(card_file, 'r') as file:
        pokemon_data = json.load(file)
        return pokemon_data

    return None

def load_pokemon_tcg_card_image(pokemon_tcg_card_id):
    folder_name = sanitize_filename(pokemon_tcg_card_id)
    file_name = sanitize_filename(f'{pokemon_tcg_card_id}.png')
    card_file = os.path.join(data_dir, folder_name)
    card_file = os.path.join(card_file, file_name)

    return Image.open(card_file).convert('RGBA')
