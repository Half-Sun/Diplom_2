import logging

import pytest
import requests

from data import UPDATE_USER_URL, CREATE_USER_URL, LOGIN_URL
from helpers import generate_unique_user, get_available_ingredients

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@pytest.fixture
def user_with_authorization():
    user_data = generate_unique_user()

    # Create user
    response = requests.post(CREATE_USER_URL, json=user_data)
    # Login user
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    response = requests.post(LOGIN_URL, json=login_data)
    access_token = response.json()["accessToken"]

    # Yield user data and access token
    yield user_data, access_token

    # Teardown: Delete the user after the test
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
    assert response.status_code == 200
    assert response.json()["success"] == True
    yield user
    requests.delete(f"{UPDATE_USER_URL}/{user['email']}", json=user)

@pytest.fixture(scope="module")
def available_ingredients():
    response = get_available_ingredients()
    assert response["success"] == True
    return response["data"]

