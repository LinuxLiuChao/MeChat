import json
import unittest

import requests


class TestEchoHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.login_url = "http://localhost:8888/login"
        self.echo_url = "http://localhost:8888/echo"

    def test_cookie(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "username": "alice",
            "password": "********"
        }
        reponse = requests.post(self.login_url, headers=headers, data=json.dumps(data))
        print(reponse.headers)

        headers['Cookie'] = "username=alice; expires=Sat, 19 Jun 2021 08:23:08 GMT; Path=/"
        # headers['Cookie'] = reponse.headers.get('Set-Cookie')
        reponse = requests.post(self.echo_url, headers=headers, data=json.dumps(data))
        print(reponse.text)

    def test_not_cookie(self):
        response = requests.get(self.echo_url)
        print("status_code: {}, text: {}".format(response.status_code, response.text))
        
