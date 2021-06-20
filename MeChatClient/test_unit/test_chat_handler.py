import unittest

from MeChatClient.me_chat_client import ChatHandler


class TestChatHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.ws_url = "ws://localhost:8888/chat"
        self.chat_cont = ChatHandler(self.ws_url)
        self.chat_cont.run_forever()

    def test_connection(self):

        print(dir(self.chat_cont))
        self.chat_cont .send_message("hello MeChat")

