import allure
import pytest
from helpers import delete_courier, accept_order, get_order_by_track, create_order, login_courier
from data import ORDER_PAYLOAD

class TestAdditionalAPI:

    @allure.title("Удаление курьера: успешный запрос")
    def test_delete_courier_success(self, courier):
        login_resp = login_courier({"login": courier["login"], "password": courier["password"]})
        courier_id = login_resp.json()["id"]
        
        response = delete_courier(courier_id)
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Удаление курьера: без id")
    def test_delete_courier_without_id(self):
        response = delete_courier("")
        assert response.status_code == 404 

    @allure.title("Принять заказ: успешный запрос")
    def test_accept_order_success(self, courier):
        order_resp = create_order(ORDER_PAYLOAD)
        track = order_resp.json()["track"]
        
        get_order_resp = get_order_by_track(track)
        order_id = get_order_resp.json()["order"]["id"]

        login_resp = login_courier({"login": courier["login"], "password": courier["password"]})
        courier_id = login_resp.json()["id"]
        
        response = accept_order(order_id, courier_id)
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Принять заказ: неверный id курьера")
    def test_accept_order_invalid_courier(self):
        order_resp = create_order(ORDER_PAYLOAD)
        track = order_resp.json()["track"]
        get_order_resp = get_order_by_track(track)
        order_id = get_order_resp.json()["order"]["id"]
        
        response = accept_order(order_id, 99999999)
        assert response.status_code == 404

    @allure.title("Получить заказ по номеру: успешный запрос")
    def test_get_order_by_track_success(self):
        order_resp = create_order(ORDER_PAYLOAD)
        track = order_resp.json()["track"]
        
        response = get_order_by_track(track)
        assert response.status_code == 200
        assert "order" in response.json()
        assert response.json()["order"]["track"] == track

    @allure.title("Получить заказ по номеру: несуществующий заказ")
    def test_get_order_by_track_not_found(self):
        response = get_order_by_track("00000000")
        assert response.status_code == 404