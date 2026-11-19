import allure
import pytest
from helpers import CourierApi
from data import ERROR_CREATE_COURIER_DUPLICATE, ERROR_CREATE_COURIER_MISSING_DATA

courier_api = CourierApi()

class TestCreateCourier:

    @allure.title("Создание курьера: успешный запрос")
    def test_create_courier_success(self, courier_data_for_creation):
        payload = courier_data_for_creation
        
        response = courier_api.create(payload)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Создание курьера: нельзя создать двух одинаковых")
    def test_create_courier_duplicate(self, courier):
        response = courier_api.create(courier)
        assert response.status_code == 409
        assert response.json()["message"] == ERROR_CREATE_COURIER_DUPLICATE

    @allure.title("Создание курьера: без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field):
        from helpers import get_random_courier_data 
        payload = get_random_courier_data()
        del payload[missing_field] 
        
        response = courier_api.create(payload)
        
        assert response.status_code == 400
        assert response.json()["message"] == ERROR_CREATE_COURIER_MISSING_DATA