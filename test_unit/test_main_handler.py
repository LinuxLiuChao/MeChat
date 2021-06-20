import unittest

import requests


class TestMainHandler(unittest.TestCase):
    def setUp(self):
        self.server_host = "http://localhost:8888"

    def test_connect(self):
        url = "{}".format(self.server_host)
        response = requests.get(url)
        print("status_code: {}, text:{}\n".format(response.status_code, response.text))
        self.assertEqual(response.status_code, 200)




if __name__ == "__main__":
    unittest.main()
