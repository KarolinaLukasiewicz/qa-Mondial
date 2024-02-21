from random import randint, random
import random
from urllib.parse import urlencode
import time

import requests

from Variables import ApiEnv, ValueStorage
from hash import get_hash_for_password

url = 'https://apigateway.epruf.pl/awp-pok/'

headers = {
    'apikey': ValueStorage.token
}


def check_possible_options(url_to_check, endpoint_name, option):
    headers = {
        "Access-Control-Request-Method": option,
        "Origin": url_to_check
    }

    response = requests.options(url_to_check, headers=headers, verify=False)
    try:
        assert "Access-Control-Allow-Methods" in response.headers, f"Expected Access-Control-Allow-Methods header in response, but got {response.headers}"
        allowed_methods = response.headers["Access-Control-Allow-Methods"]
        assert option in allowed_methods, f"Expected {option} method to be allowed, but allowed methods are: {allowed_methods}"
    except AssertionError:
        show_error_info(url_to_check, endpoint_name, response)
        raise


def show_error_info(info_url, endpoint_name, response_body):
    print("URL:")
    print(f"{info_url}")
    resp_info = f"{endpoint_name} response body:"
    print(resp_info)
    try:
        print(response_body.json())
    except Exception as e:
        print("Response body not found")


def test_get_pharmacy_status_code_200():
    response = requests.get(
        f"{url}pharmacy/ckk/23825", headers=headers, verify=False)
    assert response.status_code == 200


def test_get_notification_list_status_code_200():
    response = requests.get(
        f"{url}notification/list/00003254200000299912", headers=headers,
        verify=False)
    assert response.status_code == 200


def test_get_cards_limits_status_code_200():
    response = requests.get(
        f"{url}v1/cards-limits/00003254200000299912", headers=headers,
        verify=False)
    assert response.status_code == 200


def test_post_pos_map_status_code_200():
    def create_post():
        return {
            "latLeftBottom": 52.7,
            "latRightTop": 52.8,
            "lngLeftBottom": 18.2,
            "lngRightTop": 18.3
        }

    response = requests.post(f"{url}pos/map?onlyGpsData=true", headers=headers,
        verify=False, json=create_post())
    assert response.status_code == 200
    assert response.json()["hits"][0]["eprufCashlessService"] == True


def test_post_notification_new_check_possible_option_post():
    check_possible_options(f"{url}v2/notification/new", "post_notification_new", "POST")


def test_post_notification_new_v1_check_possible_option_post():
    check_possible_options(f"{url}notification/new", "post_notification_new_v1", "POST")


def test_get_notification_delete_check_possible_option_get():
    check_possible_options(f"{url}notification/delete/00003254200000299912/notificationNo/33333", "get_notification_delete", "GET")


def test_get_notification_status_list_check_possible_option_get():
    check_possible_options(f"{url}notification/delete/00003254200000299912/notificationNo/33333", "get_notification_status_list", "GET")


def test_post_authenticate_client_status_code_200():
    def create_post():
        return {
            "cardNumber": "00003254200015144012",
            "password": get_hash_for_password
        }

    response = requests.post(f"{url}v1/auth/client", headers=headers,
        verify=False, json=create_post())
    assert response.status_code == 200