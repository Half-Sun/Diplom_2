import logging
import random
import pytest
import requests

from data import UPDATE_USER_URL, CREATE_USER_URL, LOGIN_URL
from helpers import generate_unique_user, get_available_ingredients

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@pytest.fixture
def user_with_authorization():
    user_data = generate_unique_user()

    response = requests.post(CREATE_USER_URL, json=user_data)
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    response = requests.post(LOGIN_URL, json=login_data)
    access_token = response.json()["accessToken"]

    yield user_data, access_token

    delete_user_url = UPDATE_USER_URL
    headers = {"Authorization": f"{access_token}"}
    delete_user_response = requests.delete(delete_user_url, headers=headers)

    if delete_user_response.json().get('success', False):
        logger.info("User deleted successfully")
    else:
        logger.error(f"Failed to delete user. Response: {delete_user_response.json()}")


@pytest.fixture
def user():
    return generate_unique_user()


@pytest.fixture
def created_user(user):
    response = requests.post(CREATE_USER_URL, json=user)
    yield user
    requests.delete(f"{UPDATE_USER_URL}/{user['email']}", json=user)

@pytest.fixture(scope="module")
def available_ingredients():
    response = get_available_ingredients()
    return response["data"]


@pytest.fixture
def prepare_order_data(user_with_authorization, available_ingredients):
    user_data, access_token = user_with_authorization

    ingredients = available_ingredients

    selected_ingredients = random.sample(ingredients, 2)
    selected_ingredient_ids = [ingredient["_id"] for ingredient in selected_ingredients]

    return user_data, access_token, selected_ingredient_ids