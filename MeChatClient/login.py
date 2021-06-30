import json

import requests


def login(user_name, password):
    api = "http://localhost:9888/login"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    body = {
        "username": user_name,
        "password": password
    }
    response = requests.post(api, headers=headers, data=json.dumps(body))
    print(f"response: headers: {response.headers}, status_code: {response.status_code}, text: {response.text}")
    cookie = response.headers.get("Set-Cookie")

    return True, cookie


def echo(cookie):
    api = "http://localhost:9888/echo"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": cookie
    }
    body = "hello server"
    response = requests.post(api, headers=headers, data=body)
    print(f"response: headers: {response.headers}, status_code: {response.status_code}, text: {response.text}")


if __name__ == "__main__":
    _, cookie = login("Alice", "123456")
    echo(cookie)
