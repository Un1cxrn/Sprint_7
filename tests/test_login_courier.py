import allure
from helpers import login_courier
from data import ERROR_LOGIN_WRONG_DATA

class TestLoginCourier:

    @allure.title("Логин курьера: успешный запрос")
    def test_login_success(self, courier):
        payload = {
            "login": courier["login"],
            "password": courier["password"]
        }
        response = login_courier(payload)
        
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Логин курьера: неверный пароль")
    def test_login_wrong_password(self, courier):
        payload = {
            "login": courier["login"],
            "password": "wrong_password"
        }
        response = login_courier(payload)
        
        assert response.status_code == 404
        assert response.json()["message"] == ERROR_LOGIN_WRONG_DATA

    @allure.title("Логин курьера: несуществующий пользователь")
    def test_login_nonexistent_user(self):
        payload = {
            "login": "nonexistent_login_123",
            "password": "1234"
        }
        response = login_courier(payload)
        
        assert response.status_code == 404
        assert response.json()["message"] == ERROR_LOGIN_WRONG_DATA