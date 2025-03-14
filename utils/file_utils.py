import os
import random
import re

def sanitize_filename(filename):
    """
    Removes or replaces invalid characters from a filename to make it safe for use in Windows and other OS.
    
    Invalid characters: \ / : * ? " < > |
    Replaces them with '_'.
    
    :param filename: Original filename as a string
    :return: Sanitized filename as a string
    """
    return re.sub(r'[\/:*?"<>|]', '_', filename)

def get_random_subdirectory(directory_path):
    if not os.path.isdir(directory_path):
        raise ValueError("Provided path is not a valid directory.")
    
    # Get all subdirectories (folders)
    subdirectories = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
    
    # Return a random folder name if available, otherwise None
    return random.choice(subdirectories) if subdirectories else None


def get_random_json_path(directory_path, exclude=None):
    if not os.path.isdir(directory_path):
        raise ValueError("Provided path is not a valid directory.")
    
    # List all JSON files in the directory
    json_files = [f[:-5] for f in os.listdir(directory_path) if f.endswith('.json')]
    
    # Exclude the specified file
    if exclude and exclude in json_files:
        json_files.remove(exclude)
    
    # Return a random file name if available, otherwise None
    return random.choice(json_files) if json_files else None
