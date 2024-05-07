import pytest
import requests
from faker import Faker
from data import CREATE_ORDER_URL, CREATE_USER_URL, LOGIN_URL
from conftest import generate_unique_user

fake = Faker()

@pytest.fixture
def user_with_authorization():
    user_data = generate_unique_user()

    response = requests.post(CREATE_USER_URL, json=user_data)
    assert response.status_code == 200
    assert response.json()["success"] == True

    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    response = requests.post(LOGIN_URL, json=login_data)
    assert response.status_code == 200
    assert response.json()["success"] == True

    access_token = response.json()["accessToken"]

    return user_data, access_token

class TestCreateOrder:
    def test_create_order_with_authorization(self, user_with_authorization):
        _, access_token = user_with_authorization

        # Создаем список ингредиентов для заказа
        ingredients = ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]

        # Отправляем запрос на создание заказа с авторизацией
        response = requests.post(
            CREATE_ORDER_URL,
            json={"ingredients": ingredients},
            headers={"Authorization": f"{access_token}"},
        )

        # Проверяем, что заказ успешно создан
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "name" in response.json()
        assert "order" in response.json()
        assert "number" in response.json()["order"]
