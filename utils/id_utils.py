import string

def to_base36(n):
    # Define the alphabet for base-36 (0-9, a-z)
    alphabet = string.digits + string.ascii_lowercase
    if n == 0:
        return alphabet[0]
    digits = []
    while n:
        n, remainder = divmod(n, 36)
        digits.append(alphabet[remainder])
    return ''.join(reversed(digits))

def from_base36(base36_str):
    alphabet = string.digits + string.ascii_lowercase
    base36_dict = {char: index for index, char in enumerate(alphabet)}
    
    number = 0
    for i, char in enumerate(reversed(base36_str)):
        number += base36_dict[char] * (36 ** i)
    
    return number
