import allure
import pytest
import requests
from faker import Faker
from data import UPDATE_USER_URL, LOGIN_URL, CREATE_USER_URL
from conftest import user_with_authorization

fake = Faker()

class TestUpdateUserData:
    @allure.title("Test updating user data with authorization")
    @pytest.mark.parametrize("field", ["name", "email"])
    def test_update_user_data_with_authorization(self, user_with_authorization, field):
        user_data, access_token = user_with_authorization

        updated_data = {field: fake.name() if field == "name" else fake.email()}

        response = requests.patch(UPDATE_USER_URL, json=updated_data,
                                  headers={"Authorization": f"{access_token}"})

        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["user"][field] == updated_data[field]

    @allure.title("Test updating user data without authorization")
    @pytest.mark.parametrize("field_to_update", ["name", "email"])
    def test_update_user_data_without_authorization(self, field_to_update):
        if field_to_update == "name":
            new_value = fake.name()
        elif field_to_update == "email":
            new_value = fake.email()

        updated_data = {field_to_update: new_value}

        response = requests.patch(UPDATE_USER_URL, json=updated_data)

        assert response.status_code == 401
        assert response.json()["success"] == False
        assert response.json()["message"] == "You should be authorised"