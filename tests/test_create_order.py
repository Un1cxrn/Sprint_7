import allure
import pytest
import copy
from helpers import create_order
from data import ORDER_PAYLOAD

class TestCreateOrder:

    @allure.title("Создание заказа с разными цветами")
    @pytest.mark.parametrize("colors", [
        ["BLACK"], 
        ["GREY"], 
        ["BLACK", "GREY"], 
        []
    ])
    def test_create_order_with_colors(self, colors):
        payload = copy.deepcopy(ORDER_PAYLOAD)
        payload["color"] = colors
        
        response = create_order(payload)
        
        assert response.status_code == 201
        assert "track" in response.json()