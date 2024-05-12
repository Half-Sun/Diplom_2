import pytest, allure, requests
from data import CREATE_USER_URL, UPDATE_USER_URL
from conftest import generate_unique_user


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


class TestUserCreation:
    @allure.title("Test creating a unique user")
    def test_create_unique_user(self, user):
        response = requests.post(f"{CREATE_USER_URL}", json=user)
        assert response.status_code == 200
        assert response.json()["success"] == True

    @allure.title("Test creating an existing user")
    def test_create_existing_user(self, created_user):
        response = requests.post(f"{CREATE_USER_URL}", json=created_user)
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @allure.title("Test creating a user with missing fields")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_fields(self, user, missing_field):
        incomplete_user = user.copy()
        incomplete_user.pop(missing_field)

        response = requests.post(f"{CREATE_USER_URL}", json=incomplete_user)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"


if __name__ == "__main__":
    pytest.main()
