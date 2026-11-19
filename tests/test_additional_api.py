import allure
from helpers import CourierApi, OrdersApi
from data import ORDER_PAYLOAD

courier_api = CourierApi()
orders_api = OrdersApi()

class TestAdditionalAPI:

    @allure.title("Удаление курьера: успешный запрос")
    def test_delete_courier_success(self, courier):
        login_resp = courier_api.login({"login": courier["login"], "password": courier["password"]})
        courier_id = login_resp.json()["id"]
        
        response = courier_api.delete(courier_id)
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Удаление курьера: без id")
    def test_delete_courier_without_id(self):
        response = courier_api.delete("")
        assert response.status_code == 404 

    @allure.title("Принять заказ: успешный запрос")
    def test_accept_order_success(self, courier):
        order_resp = orders_api.create(ORDER_PAYLOAD)
        track = order_resp.json()["track"]
        
        get_order_resp = orders_api.get_by_track(track)
        order_id = get_order_resp.json()["order"]["id"]

        login_resp = courier_api.login({"login": courier["login"], "password": courier["password"]})
        courier_id = login_resp.json()["id"]
        
        response = orders_api.accept(order_id, courier_id)
        assert response.status_code in [200, 409]
        
        if response.status_code == 200:
            assert response.json() == {"ok": True}
        
        orders_api.cancel(track)

    @allure.title("Принять заказ: неверный id курьера")
    def test_accept_order_invalid_courier(self):
        order_resp = orders_api.create(ORDER_PAYLOAD)
        track = order_resp.json()["track"]
        get_order_resp = orders_api.get_by_track(track)
        order_id = get_order_resp.json()["order"]["id"]
        
        response = orders_api.accept(order_id, 99999999)
        assert response.status_code == 404
        
        orders_api.cancel(track)

    @allure.title("Получить заказ по номеру: успешный запрос")
    def test_get_order_by_track_success(self):
        order_resp = orders_api.create(ORDER_PAYLOAD)
        track = order_resp.json()["track"]
        
        response = orders_api.get_by_track(track)
        assert response.status_code == 200
        assert "order" in response.json()
        assert response.json()["order"]["track"] == track
        
        orders_api.cancel(track)

    @allure.title("Получить заказ по номеру: несуществующий заказ")
    def test_get_order_by_track_not_found(self):
        response = orders_api.get_by_track("00000000")
        assert response.status_code == 404