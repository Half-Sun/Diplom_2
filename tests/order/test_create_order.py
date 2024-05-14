import random
import logging
import allure
import requests

from conftest import user_with_authorization, available_ingredients
from data import CREATE_ORDER_URL

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TestCreateOrder:
    @allure.title("Test creating order with authorization")
    def test_create_order_with_authorization(self, user_with_authorization, available_ingredients):
        _, access_token = user_with_authorization

        ingredients = available_ingredients
        logger.info("Available ingredients: %s", ingredients)

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
    def test_create_order_without_authorization(self, available_ingredients):
        ingredients = available_ingredients

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
