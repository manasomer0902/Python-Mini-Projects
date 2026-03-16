# How to create a random password from python code

import random
import  string

def generate_password(length = 12, include_digits = True, include_special_chars = True):
    # Define Character sets
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits if include_digits else ""
    special_chars = string.punctuation if include_special_chars else  ""

    # Combine character sets based on options
    characters = uppercase_letters + lowercase_letters + digits + special_chars

    # check if the character set is empty
    if not characters:
        raise ValueError("No characters available for password generator.")

    # Generate the password
    password = ''.join(random.choice(characters)for _ in range(length))

    return password

# Example usage

password = generate_password()
print(password)
