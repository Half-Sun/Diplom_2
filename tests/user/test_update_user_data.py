import allure
import requests
from faker import Faker
from data import UPDATE_USER_URL
from conftest import user_with_authorization

fake = Faker()

class TestUpdateUserData:
    @allure.title("Test updating user name with authorization")
    def test_update_user_name_with_authorization(self, user_with_authorization):
        user_data, access_token = user_with_authorization

        updated_name = fake.name()

        response = requests.patch(UPDATE_USER_URL, json={"name": updated_name},
                                  headers={"Authorization": f"{access_token}"})

        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["user"]["name"] == updated_name

    @allure.title("Test updating user email with authorization")
    def test_update_user_email_with_authorization(self, user_with_authorization):
        user_data, access_token = user_with_authorization

        updated_email = fake.email()

        response = requests.patch(UPDATE_USER_URL, json={"email": updated_email},
                                  headers={"Authorization": f"{access_token}"})

        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["user"]["email"] == updated_email

    @allure.title("Test updating user data without authorization")
    def test_update_user_data_without_authorization(self):
        response = requests.patch(UPDATE_USER_URL, json={"name": fake.name()})

        assert response.status_code == 401
        assert response.json()["success"] == False
        assert response.json()["message"] == "You should be authorised"
