import tornado.web
import tornado.websocket
import jwt
from common.const_str import USER_NAME, JWT_TOKEN, EXP
from web_handler.status_const import response_msg

jwt_key = "7460d7cb-bcea-4fbe-87ec-d116123beda4"
jwt_algorithm = "HS256"


class MeBase:
    def __init__(self):
        self.client_address = None


class BaseHandler(tornado.web.RequestHandler):
    def create_jwt_token(self, user_name, expires_time):
        payload = {
            USER_NAME: user_name,
            EXP: expires_time
        }
        return jwt.encode(payload, key=jwt_key, algorithm=jwt_algorithm)

    def get_current_user(self):
        jwt_token = self.get_secure_cookie(JWT_TOKEN)
        try:
            data = jwt.decode(jwt_token, jwt_key, algorithms=jwt_algorithm)
        except Exception as err:
            print("jwt.decode Exception: {}".format(err))
            return None
        return data.get(USER_NAME)

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
