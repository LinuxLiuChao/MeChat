import json
import unittest

import requests

from common.const_str import RESPONSE_CODE, USER_NAME, PASSWORD
from web_handler.status_const import Status


class TestLogOutHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "http://localhost:8888/logout"

    def test_log_out_failed(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        res = requests.post(self.url, headers=headers)
        self.assertEqual(res.status_code, 403)

    def test_log_out_success(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            USER_NAME: "Alice",
            PASSWORD: "123456"
        }

        response = requests.post(self.url.replace("logout", "login"), headers=headers, data=json.dumps(data))
        headers['Cookie'] = response.headers.get('Set-Cookie')
        res = requests.post(self.url, headers=headers)
        cookie = res.json().get('Cookie')
        self.assertIsNone(cookie)
        self.assertEqual(res.json().get(RESPONSE_CODE), Status.SUCCESS.value)
