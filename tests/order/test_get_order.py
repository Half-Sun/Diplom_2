import random
import allure
from data import CREATE_ORDER_URL, GET_ORDERS_URL
from conftest import user_with_authorization, get_available_ingredients
import requests




class TestCreateUserOrderAndRetrieveOrders:
    @allure.title("Test creating user order and retrieving orders without authorization")
    def test_create_user_order_and_get_orders_without_authorization(self):

        response = get_available_ingredients()
        assert response["success"] == True

        ingredients = response["data"]

        selected_ingredients = random.sample(ingredients, 2)

        selected_ingredient_ids = [ingredient["_id"] for ingredient in selected_ingredients]

        response = requests.post(
            CREATE_ORDER_URL,
            json={"ingredients": selected_ingredient_ids},
        )

        assert response.status_code == 200
        assert response.json()["success"] == True

        response = requests.get(GET_ORDERS_URL)
        assert response.status_code == 401
        assert response.json()["message"] == "You should be authorised"

    @allure.title("Test creating user order and retrieving orders with authorization")
    def test_create_user_order_and_get_orders_with_authorization(self, user_with_authorization):
        user_data, access_token = user_with_authorization

        response = get_available_ingredients()
        assert response["success"] == True

        ingredients = response["data"]
        print("Available ingredients:", ingredients)

        assert all(isinstance(ingredient, dict) for ingredient in ingredients)

        selected_ingredients = random.sample(ingredients, 2)

        selected_ingredient_ids = [ingredient["_id"] for ingredient in selected_ingredients]

        response = requests.post(
            CREATE_ORDER_URL,
            json={"ingredients": selected_ingredient_ids},
            headers={"Authorization": f"{access_token}"},
        )

        assert response.status_code == 200
        assert response.json()["success"] == True

        response = requests.get(GET_ORDERS_URL, headers={"Authorization": f"{access_token}"})
        assert response.status_code == 200
        assert "orders" in response.json()
