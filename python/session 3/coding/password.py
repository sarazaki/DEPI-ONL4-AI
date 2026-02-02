import random
import string

def generate_password(length):
    characters = string.ascii_letters + string.digits
    password = ""

    for _ in range(length):
        password += random.choice(characters)

    return password
