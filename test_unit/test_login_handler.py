import json
import sys
import unittest

import requests

from common.const_str import RESPONSE_CODE, USER_NAME, PASSWORD
from web_handler.status_const import Status


class TestRouterHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "http://localhost:8888/login"

    def test_re_login(self):
        reponse = requests.get(self.url)
        print("{} status_code: {} text: {}".format(sys._getframe().f_code.co_name, reponse.status_code, reponse.text))
        self.assertEqual(reponse.json().get(RESPONSE_CODE), Status.RE_LOG_IN.value)

    def test_login_success(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            USER_NAME: "Alice",
            PASSWORD: "123456"
        }
        reponse = requests.post(self.url, headers=headers, data=json.dumps(data))
        print("{} status_code: {} text: {}".format(sys._getframe().f_code.co_name, reponse.status_code, reponse.text))
        self.assertEqual(reponse.json().get(RESPONSE_CODE), Status.SUCCESS.value)

    def test_login_failed(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            USER_NAME: "Bob",
            PASSWORD: "123456"
        }

        reponse = requests.post(self.url, headers=headers, data=json.dumps(data))
        print("{} status_code: {} text: {}".format(sys._getframe().f_code.co_name, reponse.status_code, reponse.text))
        self.assertEqual(reponse.json().get(RESPONSE_CODE), Status.INVALID_PASSWORD.value)






