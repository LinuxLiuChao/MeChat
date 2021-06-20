import tornado.web
import tornado.websocket
from common.const_str import USER_NAME
from web_handler.status_const import response_msg


class MeBase:
    def __init__(self):
        self.client_address = None


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_cookie(USER_NAME)

    def response_cli(self, code):

        self.write(response_msg(code))


class WsBaseHandler(tornado.websocket.WebSocketHandler, MeBase):
    def open(self):
        self.client_address = self.request.connection.context.address
        print("websocket connection success")

    def on_close(self):
        pass

    def on_message(self, message):
        pass
