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
    # Get all subdirectories (folders)
    subdirectories = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
    
    if not subdirectories:
        return None  # In case there are no subdirectories
    
    # Pick a random folder name (ID)
    random_subdirectory = random.choice(subdirectories)
    return random_subdirectory
