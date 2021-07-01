import json

import requests
from me_chat_client import MeChatClient


class HandlerProcess(MeChatClient):
    def __init__(self, url):
        super().__init__(url)
        self.cookie = None
        self._handler = {
            "login": self.login,
            "logout": self.logout,
            "chat": self.chat
        }
        self.user_name = None
        self.password = None
        self.on_line = False
        self.run()

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
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            body = {
                "user_name": self.user_name,
                "password": self.password
            }
            url = "http://localhost:9888/login"
            response = requests.post(url, headers=headers, data=json.dumps(body))
            if response.status_code != 200:
                print(f"requests ({url}) failed. status_code:{response.status_code}, text:{response.text}")
                return
            print(f"requests ({url}) success. status_code:{response.status_code}, text:{response.text}, headers:{response.headers}, cookie:{response.cookies}")

            print(f"login success")
            cookie = response.cookies
            self.set_cookie(cookie)
            self.on_line = True
        except Exception as err:
            print(f"login Exception: {err}")

    def logout(self, *args):
        print(f"call logout success. {args}")
        self.on_line = False

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
