import random
import allure
import requests
from data import CREATE_ORDER_URL
from conftest import get_available_ingredients, user_with_authorization



class TestCreateOrder:
    @allure.title("Test creating order with authorization")
    def test_create_order_with_authorization(self, user_with_authorization):
        _, access_token = user_with_authorization

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

    @allure.title("Test creating order without authorization")
    def test_create_order_without_authorization(self):
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

    @allure.title("Test creating order without ingredients")
    def test_create_order_without_ingredients(self):
        response = requests.post(
            CREATE_ORDER_URL,
            json={"ingredients": []},
        )

        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Test creating order with invalid ingredients hash")
    def test_create_order_with_invalid_ingredients_hash(self):

        response = requests.post(
            CREATE_ORDER_URL,
            json={"ingredients": ["invalid_hash1", "invalid_hash2"]},
        )

        assert response.status_code == 500
