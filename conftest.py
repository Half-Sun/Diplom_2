import string
import random

import pytest
import requests
from faker import Faker

from data import GET_INGREDIENTS_URL, LOGIN_URL, CREATE_USER_URL

fake = Faker()

def generate_unique_user():
    email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@example.com"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    name = ''.join(random.choices(string.ascii_uppercase, k=6))

    return {"email": email, "password": password, "name": name}


def get_available_ingredients():
    response = requests.get(GET_INGREDIENTS_URL)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch ingredients. Status code: {response.status_code}")

    return response.json()

@pytest.fixture
def user_with_authorization(request):
    user_data = generate_unique_user()

    # Create user
    response = requests.post(CREATE_USER_URL, json=user_data)
    assert response.status_code == 200
    assert response.json()["success"] == True

    # Login user
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    response = requests.post(LOGIN_URL, json=login_data)
    assert response.status_code == 200
    assert response.json()["success"] == True

    access_token = response.json()["accessToken"]

    # Yield user data and access token
    yield user_data, access_token

    # Teardown: Delete the user after the test
    delete_user_url = "https://stellarburgers.nomoreparties.site/api/auth/user"
    headers = {"Authorization": f"{access_token}"}
    delete_user_response = requests.delete(delete_user_url, headers=headers)

    if delete_user_response.json().get('success', False):
        print("User deleted successfully")
    else:
        print(f"Failed to delete user. Response: {delete_user_response.json()}")

