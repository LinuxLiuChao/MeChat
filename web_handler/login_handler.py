import json
import time

from common.const_str import USER_NAME, PASSWORD, JWT_TOKEN
from common.settings import cookie_expires_time
from web_handler.base_handler import BaseHandler
from web_handler.status_const import Status, response_msg

users_info = [
    {
        USER_NAME: "Alice",
        PASSWORD: "123456"
    },
    {
        USER_NAME: "Bob",
        PASSWORD: "123456"
    }
]


class LoginHandler(BaseHandler):
    def get(self):
        return self.response_cli(Status.RE_LOG_IN)

    def post(self):
        body = json.loads(self.request.body)
        user_name = body.get(USER_NAME)
        password = body.get(PASSWORD)

        ret = list(filter(lambda x: x[USER_NAME] == user_name and x[PASSWORD] == password, users_info))
        if not ret:
            return self.write(response_msg(Status.INVALID_PASSWORD))

        expires_time = time.time() + cookie_expires_time

        token = self.create_jwt_token(user_name, expires_time)
        self.set_secure_cookie(name=JWT_TOKEN, value=token, expires=expires_time)
        return self.response_cli(Status.SUCCESS)
