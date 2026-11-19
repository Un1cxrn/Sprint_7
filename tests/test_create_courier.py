import allure
import pytest
from helpers import CourierApi, get_random_courier_data
from data import ERROR_CREATE_COURIER_DUPLICATE, ERROR_CREATE_COURIER_MISSING_DATA

courier_api = CourierApi()

class TestCreateCourier:

    @allure.title("Создание курьера: успешный запрос")
    def test_create_courier_success(self):
        payload = get_random_courier_data()
        response = courier_api.create(payload)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        try:
            login_resp = courier_api.login({"login": payload["login"], "password": payload["password"]})
            courier_id = login_resp.json()["id"]
        finally:
            if login_resp.status_code == 200:
                courier_api.delete(courier_id)

    @allure.title("Создание курьера: нельзя создать двух одинаковых")
    def test_create_courier_duplicate(self, courier):
        response = courier_api.create(courier)
        assert response.status_code == 409
        assert response.json()["message"] == ERROR_CREATE_COURIER_DUPLICATE

    @allure.title("Создание курьера: без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field):
        payload = get_random_courier_data()
        del payload[missing_field] 
        response = courier_api.create(payload)
        assert response.status_code == 400
        assert response.json()["message"] == ERROR_CREATE_COURIER_MISSING_DATA