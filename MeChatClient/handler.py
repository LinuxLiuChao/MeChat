import json

import requests
from me_chat_client import MeChatClient

from base_requests import RequestBase


class HandlerProcess(MeChatClient):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.cookies = None
        self._handler = {
            "login": self.login,
            "logout": self.logout,
            "chat": self.chat
        }
        # self.user_name = None
        # self.password = None
        self.on_line = False
        self._request = RequestBase(host, port)

    def login(self, *args):
        if len(args) != 3:
            print(f"params is wrong({args}), usage: login <username> <password>\n")
            return
        if self.on_line:
            print(f"user_name: {self.user_name} is online. please logout first.\n")
            return

        _, self.user_name, self.password = args

        try:
            print(f"login {self.user_name}, {self.password}")
            if self._request.login(self.user_name, self.password):
                self.on_line = True
                if self.is_connected is False:
                    self.set_cookies(self._request._cookies)
                    print(f"request._cookies: {self._request._cookies['jwt_token']}")
                    self.run()
        except Exception as err:
            print(f"login Exception: {err}")

    def logout(self, *args):
        status_code, text = self._request.logout()
        if status_code == 200:
            print(f"[logout] success. {args}")
            self.on_line = False
            self.user_name, self.password = None, None
            self.ws_cli.close()
            self.is_connected = False
            self.ws_cli = None
            return True
        print(f"[logout] failed. status_code:{status_code}, message: {text}")
        return False

    def chat(self, *args):
        print(f"call chat success. {args}")
        if len(args) != 3:
            print(f"params is wrong({args}), usage: chat <username> <message>\n")
            return
        _, to_user, message = args
        self.send_message_to_user(to_user, message)

    def handler(self, *args):
        cmd = args[0]
        if cmd not in self._handler:
            print("Input command incorrect")
            return None
        return self._handler[cmd](*args)
