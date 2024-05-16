
import allure
from data import CREATE_ORDER_URL, GET_ORDERS_URL
from conftest import prepare_order_data, available_ingredients, user_with_authorization

import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestCreateUserOrderAndRetrieveOrders:

    @allure.title("Test creating user order and retrieving orders without authorization")
    def test_create_user_order_and_get_orders_without_authorization(self, prepare_order_data):
        user_data, access_token, selected_ingredient_ids = prepare_order_data

        response = requests.post(
            CREATE_ORDER_URL,
            json={"ingredients": selected_ingredient_ids},
        )

        assert response.status_code == 200
        assert response.json()["success"] == True

        response = requests.get(GET_ORDERS_URL)
        assert response.status_code == 401
        assert response.json()["message"] == "You should be authorised"
        logger.info("Attempt to get orders without authorization: %s", response.json())


    @allure.title("Test creating user order and retrieving orders with authorization")
    def test_create_user_order_and_get_orders_with_authorization(self, prepare_order_data):
        user_data, access_token, selected_ingredient_ids = prepare_order_data

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
        logger.info("Orders retrieved with authorization: %s", response.json())