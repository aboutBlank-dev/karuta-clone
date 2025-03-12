import os
import argparse
import requests
import json
from PIL import Image
from io import BytesIO

# Create directories for storing data
data_dir = 'pokemon_data'

# Ensure the main directory exists
os.makedirs(data_dir, exist_ok=True)

# Function to download and save all sprites for a Pokémon
def download_sprites(sprites, pokemon_id):
    # Create folder for the Pokémon by ID
    pokemon_folder = os.path.join(data_dir, str(pokemon_id))
    os.makedirs(pokemon_folder, exist_ok=True)

    for sprite_key, sprite_url in sprites.items():
        if isinstance(sprite_url, dict):
            download_sprites(sprite_url, pokemon_id)
        elif sprite_url:  # Only download if the URL is not None
            try:
                # Download the sprite image
                response = requests.get(sprite_url)
                response.raise_for_status()  # Raise an exception if there's an error

                # Save the image in the appropriate file
                sprite_name = sprite_key + ".png"
                try:
                    img = Image.open(BytesIO(response.content))
                    img.save(os.path.join(pokemon_folder, sprite_name))
                except Exception as e:
                    print(f"Error saving {sprite_key} for Pokémon ID {pokemon_id} Sprite Url: {sprite_url} Error: {e}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading {sprite_key} for Pokémon ID {pokemon_id}: {e}")


def fetch_pokemon_data(pokemon_name, force=False):
    print(f"Fetching data for {pokemon_name}...")
    pokemon_info = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}").json()
    pokemon_id = pokemon_info['id']

    pokemon_folder = os.path.join(data_dir, str(pokemon_id))
    if os.path.exists(pokemon_folder) and not force:
        print(f"Skipping Pokémon ID {pokemon_id} ({pokemon_name}) as it already exists.")
        return
    
    # Remove the "moves" key from the data
    if 'moves' in pokemon_info:
        del pokemon_info['moves']
    
    # Download all sprite images
    if 'sprites' in pokemon_info:
        download_sprites(pokemon_info['sprites'], pokemon_id)
    
    # Save the Pokémon's data in a JSON file by ID (excluding "moves")
    with open(os.path.join(data_dir, f'{pokemon_id}.json'), 'w') as file:
        json.dump(pokemon_info, file, indent=2)
    
    return pokemon_info

def fetch_all_pokemon_data(force=False):
    pokemon_data = []
    base_url = "https://pokeapi.co/api/v2/pokemon"
    
    # Fetch initial page
    response = requests.get(base_url)
    response.raise_for_status()
    data = response.json()

    # Loop through each page of Pokémon data
    while data:
        for pokemon in data['results']:
            pokemon_name = pokemon['name']
            
            # Get detailed information for each Pokémon
            pokemon_info = fetch_pokemon_data(pokemon_name)

            # Add the data to our list
            pokemon_data.append(pokemon_info)
        
        # Check if there's a next page and continue
        if 'next' in data and data['next']:
            response = requests.get(data['next'])
            response.raise_for_status()
            data = response.json()
        else:
            break
    
    print(f"Finished fetching {len(pokemon_data)} Pokémon!")

def main():
    parser = argparse.ArgumentParser(description="Download Pokémon sprites.")
    parser.add_argument("pokemon", type=str, help="Pokemon ID or 'all' to fetch all Pokémon.")
    parser.add_argument("--force", action="store_true", help="Force the download of the Pokémon data.")
    
    args = parser.parse_args()

    if args.pokemon == "all":
        fetch_all_pokemon_data(args.force)  # Fetch and process all Pokémon
    else:
        try:
            pokemon_id = int(args.pokemon)
            fetch_pokemon_data(pokemon_id, args.force)
        except ValueError:
            print("[ERROR] Invalid Pokémon ID. Please provide a valid number or 'all'.")

if __name__ == "__main__":
    main()

# Function to load Pokémon data and display a sprite (example)
def load_pokemon_data(pokemon_id):
    # Load Pokémon data from JSON file
    pokemon_file = os.path.join(data_dir, f'{pokemon_id}.json')
    with open(pokemon_file, 'r') as file:
        pokemon_data = json.load(file)
    
    # Load every .png file in the Pokémon's folder
    pokemon_folder = os.path.join(data_dir, str(pokemon_id))
    pokemon_data["images"] = {}
    for file_name in os.listdir(pokemon_folder):
        if file_name.endswith('.png'):
            name_without_extension = os.path.splitext(file_name)[0]
            pokemon_data["images"][name_without_extension] = Image.open(os.path.join(pokemon_folder, file_name)).convert('RGBA')
    return pokemon_data
