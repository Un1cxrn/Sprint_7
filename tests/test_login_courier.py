import allure
from helpers import CourierApi
from data import ERROR_LOGIN_WRONG_DATA

courier_api = CourierApi()

class TestLoginCourier:

    @allure.title("Логин курьера: успешный запрос")
    def test_login_success(self, courier):
        response = courier_api.login({"login": courier["login"], "password": courier["password"]})
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Логин курьера: неверный пароль")
    def test_login_wrong_password(self, courier):
        response = courier_api.login({"login": courier["login"], "password": "wrong_password"})
        assert response.status_code == 404
        assert response.json()["message"] == ERROR_LOGIN_WRONG_DATA

    @allure.title("Логин курьера: несуществующий пользователь")
    def test_login_nonexistent_user(self):
        response = courier_api.login({"login": "nonexistent_login_123", "password": "1234"})
        assert response.status_code == 404
        assert response.json()["message"] == ERROR_LOGIN_WRONG_DATA