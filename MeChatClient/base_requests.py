import json

import requests

from const_def import USERNAME, PASSWORD


class RequestBase:
    def __init__(self, host, port):
        self._host = f"http://{host}:{port}"
        self._headers = None
        self._cookies = None
        self._body = None
        self.user_name = None
        self.password = None

    def set_headers(self,  use_default=True, **extra_data):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if use_default is False: headers = {}
        if extra_data:
            headers.update(extra_data)
        self._headers = headers if headers else None

    def set_cookie(self, kwargs):
        if kwargs and isinstance(kwargs, dict): self._cookies = kwargs

    def get_cookie(self, cookies=None, key=None):
        if all((key, key)): return cookies.get(key)

    def set_cookies(self, response):
        if hasattr(response, 'cookies'):
            self._cookies = response.cookies
        else:
            print(f'set_cookies: invalid param({response})')

    def _post(self, api, body):
        url = self._host + api
        if isinstance(body, dict):
            body = json.dumps(body)
        else:
            print(f"[post: {api}] body ({body}) invalid")
            body = None
        response = requests.post(url, headers=self._headers, data=body, cookies=self._cookies)
        print(f"response: {response.status_code}, {response.text}")
        self.set_cookies(response)
        return response.status_code, response.text

    def login(self, user_name=None, password=None):
        if user_name and password:
            self.user_name = user_name
            self.password = password

        if not (self.user_name and self.password):
            print(f"[login] Please login before.")
            return False

        body = {
            USERNAME: self.user_name,
            PASSWORD: self.password
        }
        status_code, text = self._post("/login", body)
        message = json.loads(text)
        if status_code == 200 and message.get("code") == 200:
            return True
        return False

    def logout(self):
        return self._post("/logout", None)

    def post(self, api, body=None):
        status_code, text = self._post(api, body)
        if status_code == 403:
            if self.login():
                return self._post(api, body)
        return status_code, text
