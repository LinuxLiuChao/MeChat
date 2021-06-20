import time

import tornado.web

from web_handler.base_handler import BaseHandler


class EchoHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        print("login: {}".format(self.request.headers))
        cookie = self.get_cookie("username")

        print("EchoHandler get cookie: {}".format(cookie))
        self.write("hello client")

    @tornado.web.authenticated
    def post(self):
        print("request header: {}".format(self.request.headers))
        cookie = self.get_cookie("username")
        expires_time = self.get_cookie("expires")
        print("expires_time: {}".format(expires_time))
        self.clear_all_cookies()
        print("EchoHandler get cookie: {}".format(cookie))
