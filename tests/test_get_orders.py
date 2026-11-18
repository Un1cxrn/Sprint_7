import allure
import requests
from data import BASE_URL

class TestGetOrders:

    @allure.title("Получение списка заказов")
    def test_get_orders(self):
        response = requests.get(f"{BASE_URL}/api/v1/orders")
        
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)