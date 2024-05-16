import allure
import requests
from data import CREATE_USER_URL, LOGIN_URL, UPDATE_USER_URL
from conftest import user

class TestUserLogin:
    @allure.title("Test login for existing user")
    def test_login_existing_user(self, user):
        response = requests.post(CREATE_USER_URL, json=user)
        assert response.status_code == 200

        response = requests.post(LOGIN_URL, json=user)
        assert response.status_code == 200
        assert response.json()["success"] == True
        requests.delete(f"{UPDATE_USER_URL}/{user['email']}", json=user)
    @allure.title("Test login with wrong credentials")
    def test_login_wrong_credentials(self):
        wrong_user = {"email": "wrong_email@example.com", "password": "wrong_password"}
        response = requests.post(LOGIN_URL, json=wrong_user)
        assert response.status_code == 401
        assert response.json()["success"] == False
        assert response.json()["message"] == "email or password are incorrect"
