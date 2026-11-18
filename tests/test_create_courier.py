import allure
import pytest
from helpers import create_courier, get_random_courier_data
from data import ERROR_CREATE_COURIER_DUPLICATE, ERROR_CREATE_COURIER_MISSING_DATA

class TestCreateCourier:

    @allure.title("Создание курьера: успешный запрос")
    def test_create_courier_success(self):
        payload = get_random_courier_data()
        response = create_courier(payload)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Создание курьера: нельзя создать двух одинаковых")
    def test_create_courier_duplicate(self, courier):
        response = create_courier(courier)
        
        assert response.status_code == 409
        assert response.json()["message"] == ERROR_CREATE_COURIER_DUPLICATE

    @allure.title("Создание курьера: без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field):
        payload = get_random_courier_data()
        del payload[missing_field] 
        
        response = create_courier(payload)
        
        assert response.status_code == 400
        assert response.json()["message"] == ERROR_CREATE_COURIER_MISSING_DATA