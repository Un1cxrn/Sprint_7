import pytest
from helpers import get_random_courier_data, CourierApi
from data import ORDER_PAYLOAD
import copy

courier_api = CourierApi()

@pytest.fixture
def courier():
    payload = get_random_courier_data()
    courier_api.create(payload)
    
    yield payload
    
    login_response = courier_api.login({
        "login": payload["login"], 
        "password": payload["password"]
    })
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        courier_api.delete(courier_id)