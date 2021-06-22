import json
import sqlite3
import time

from common.const_str import USER_NAME, PASSWORD, JWT_TOKEN
from common.settings import cookie_expires_time, sqlite3_host
from web_handler.base_handler import BaseHandler
from web_handler.status_const import Status, response_msg


class LoginHandler(BaseHandler):
    def get(self):
        return self.response_cli(Status.RE_LOG_IN)

    def post(self):
        body = json.loads(self.request.body)
        user_name = body.get(USER_NAME)
        password = body.get(PASSWORD)

        if self.user_format_is_valid(user_name, password) is False:
            return self.write(response_msg(Status.INVALID_PASSWORD))

        if self.user_is_valid(user_name, password) is False:
            return self.write(response_msg(Status.INVALID_PASSWORD))

        expires_time = time.time() + cookie_expires_time

        token = self.create_jwt_token(user_name, expires_time)
        self.set_secure_cookie(name=JWT_TOKEN, value=token, expires=expires_time)
        return self.response_cli(Status.SUCCESS)

    def user_is_valid(self, user, password):
        db_conn = sqlite3.connect(sqlite3_host)
        cursor = db_conn.cursor()
        try:
            sql = f"""select count(*) from user where user_name='{user}' and password='{password}';"""
            print(f"sql_statement: {sql}")
            cursor.execute(sql)
            ret = cursor.fetchone()[0]
            cursor.close()
            db_conn.close()
            print(f"{ret}")
            return ret != 0
        except Exception as err:
            print("user_is_valid: Exception {}".format(err))
            cursor.close()
            db_conn.close()
            return False

    def user_format_is_valid(self, user, password):
        if user.find(" ") != -1 or password.find(" ") != -1:
            return False
        return True
