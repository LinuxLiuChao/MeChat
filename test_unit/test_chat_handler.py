import json
import unittest

import requests


class TestChatHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "http://localhost:8888/chat"

    def test_ws_connect(self):
        pass