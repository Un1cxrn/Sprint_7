import random
import string
import requests
import allure
from data import BASE_URL

def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def get_random_courier_data():
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

class CourierApi:
    @allure.step("Создание курьера")
    def create(self, payload):
        return requests.post(f"{BASE_URL}/api/v1/courier", data=payload)

    @allure.step("Логин курьера")
    def login(self, payload):
        return requests.post(f"{BASE_URL}/api/v1/courier/login", data=payload)

    @allure.step("Удаление курьера")
    def delete(self, courier_id):
        return requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")

class OrdersApi:
    @allure.step("Создание заказа")
    def create(self, payload):
        return requests.post(f"{BASE_URL}/api/v1/orders", json=payload)

    @allure.step("Отмена заказа")
    def cancel(self, track):
        return requests.put(f"{BASE_URL}/api/v1/orders/cancel", params={"track": track})

    @allure.step("Принятие заказа")
    def accept(self, order_id, courier_id):
        return requests.put(f"{BASE_URL}/api/v1/orders/accept/{order_id}", params={"courierId": courier_id})

    @allure.step("Получение заказа по треку")
    def get_by_track(self, track):
        return requests.get(f"{BASE_URL}/api/v1/orders/track", params={"t": track})