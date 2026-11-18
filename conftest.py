import pytest
from helpers import get_random_courier_data, create_courier, login_courier, delete_courier

@pytest.fixture
def courier():
    payload = get_random_courier_data()
    create_courier(payload)
    
    yield payload
    
    login_response = login_courier({
        "login": payload["login"], 
        "password": payload["password"]
    })
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        delete_courier(courier_id)