import asyncio
import json
import time
from threading import Thread

import websocket


class ChatHandler:
    def __init__(self, host, port):
        url = f"ws://{host}:{port}/chat"
        self.ws_cli = websocket.WebSocketApp(url,
                                             on_open=self.on_open,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close)
        self.is_connected = False
        self.user_name = None
        self.user_id = None
        # print(dir(self.ws_cli))

    def on_open(self, ws):
        print("open connection success!!!\n")
        self.is_connected = True
        ws.send({"username": "Alice"})
        print("on_open : {}".format(ws.recv()))
        pass

    def on_message(self, ws, message):
        message = json.loads(message)
        status = message.get("status")
        print("on_message: {}".format(message))
        if message.get("type") == "login":
            print("login status: {}".format(status))
            if message.get("type") == "login" and status == "success":
                self.user_id = message.get("text")
            return

        from_user, from_msg = message.get("from"), message.get("message")
        if any((from_user, from_msg)) is False: return

        print("from {}: {} \n>>>:".format(from_user, from_msg))

    def on_error(self, ws, error):
        print("on_error: err{}".format(error))
        pass

    def on_close(self, ws):
        print("ws closed")
        self.is_connected = False

    def send_message(self, message):
        if isinstance(message, dict):
            message = json.dumps(message)

        for t in range(3):
            if self.is_connected:
                self.ws_cli.send(message)
                break
            time.sleep(1)
        else:
            print("Please connect server first")

    def run_forever(self):
        print("connecting to server")
        try:
            self.ws_cli.run_forever()
        except Exception as err:
            print("run_forever Exception: {}".format(err))
        finally:
            time.sleep(1)
            self.run_forever()

    def set_cookie(self, cookie):
        self.ws_cli.cookie = cookie


class MeChatClient(ChatHandler):
    def run(self):
        Thread(target=self.run_forever).start()

    def send_user_info(self, user_name):
        user_info = {
            "type": "login",
            "username": user_name
        }
        self.user_name = user_name
        self.send_message(user_info)

    def send_message_to_user(self, to_user, message):
        message = {
            "type": "chat",
            "from": self.user_id,
            "to": to_user,
            "message": message
        }
        self.send_message(message)


if __name__ == "__main__":
    user_name = input("Please input your name: ")
    to_user = input("Please input send to message user_name: ")
    client = MeChatClient("ws://localhost:9888/chat")
    client.run()
    client.send_user_info(user_name)
    while True:
        message = input(">>>: ")
        client.send_message_to_user(to_user, message)
