import random
import string
import requests
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

def create_courier(payload):
    return requests.post(f"{BASE_URL}/api/v1/courier", data=payload)

def login_courier(payload):
    return requests.post(f"{BASE_URL}/api/v1/courier/login", data=payload)

def delete_courier(courier_id):
    return requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")

def create_order(payload):
    return requests.post(f"{BASE_URL}/api/v1/orders", json=payload)

def delete_courier(courier_id):
    return requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")

def accept_order(order_id, courier_id):
    
    return requests.put(f"{BASE_URL}/api/v1/orders/accept/{order_id}", params={"courierId": courier_id})

def get_order_by_track(track):
    
    return requests.get(f"{BASE_URL}/api/v1/orders/track", params={"t": track})