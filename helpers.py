import random
import string
import requests
from faker import Faker

fake = Faker()

from data import GET_INGREDIENTS_URL


def generate_unique_user():
    email = ''.join(random.choice(string.ascii_lowercase) for _ in range(8)) + "@example.com"
    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    name = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))

    return {"email": email, "password": password, "name": name}


def get_available_ingredients():
    response = requests.get(GET_INGREDIENTS_URL)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch ingredients. Status code: {response.status_code}")

    return response.json()
