import datetime
import json
import sqlite3

from common.settings import sqlite3_host
from web_handler.base_handler import WsBaseHandler
from web_handler.status_const import MessageStatus

connections = {
    "user_name": "session"
}
address = {
    "(host,ip)": "usr_name"
}


class ChatHandler(WsBaseHandler):
    def on_message(self, message):
        print("receive message: {}".format(message))
        message = json.loads(message)
        msg_type = message.pop("type")
        if msg_type == "login":
            user_name = message.get("username")
            user_id = self.user_is_exist(user_name)
            if user_id is None:
                self.write_message({"type": "login", "status": "failed", "text": "{} is not exist".format(user_name)})
                return

            print("response client: {}".format(str(user_id)))
            self.write_message({"type": "login", "status": "success", "text": "{}".format(str(user_id))})

            self.send_no_read_message(user_id)

            connection = connections.get(user_name)
            if connection:
                print("connection already exist. user_name: {}".format(user_name))
                connection.close()

                connections[user_name] = self
            else:
                print("Create new connection. user_name: {}".format(user_name))
                connections[user_name] = self
            address[self.client_address] = user_name

        if msg_type == "chat":
            to_user = message.get("to")
            to_user_id = self.user_is_exist(to_user)
            if to_user_id is None:
                print(f"{to_user} is not exist")
                self.write_message({"type": "login", "status": "failed", "text": "{} is not exist".format(to_user)})
                return
            message["to"] = to_user_id

            to_user_connect = connections.get(to_user)
            if not to_user_connect:
                print("to_user disOnline")
                self.record_message(message, MessageStatus.FAILED.value)
                self.write_message({"status": "failed", "text": "{} disOnline".format(to_user)})
                return

            try:
                to_user_connect.write_message(message)
            except Exception as err:
                print("send to {} failed; err={}".format(to_user, err))
                self.record_message(message, MessageStatus.FAILED.value)
                return
            self.record_message(message, MessageStatus.SUCCESS.value)
            print("send to {} success".format(to_user))

    def on_close(self):
        user_name = address.get(self.client_address)
        if user_name:
            connections.pop(user_name)
        print("websocket connection({}:{}) closed.".format(user_name, self.client_address))

    def user_is_exist(self, to_user):
        db_conn = sqlite3.connect(sqlite3_host)
        cursor = db_conn.cursor()
        try:
            sql = f"""select id from user where user_name='{to_user}';"""
            print(f"sql_statement: {sql}")
            cursor.execute(sql)
            ret = cursor.fetchone()[0]
            cursor.close()
            db_conn.close()
            print(f"{ret}")
            return ret
        except Exception as err:
            print("user_is_valid: Exception {}".format(err))
            cursor.close()
            db_conn.close()
            return None

    def record_message(self, message, status):
        db_conn = sqlite3.connect(sqlite3_host)
        cursor = db_conn.cursor()
        from_user = message.get("from")
        to_user = message.get("to")
        msg_text = message.get("message")

        try:
            sql = f"""insert into message (from_user_id, to_user_id, message, status) values ({from_user}, {to_user}, '{msg_text}', {status});"""
            print(f"sql_statement: {sql}")
            cursor.execute(sql)
            db_conn.commit()
            cursor.close()
            db_conn.close()
            return True
        except Exception as err:
            print("user_is_valid: Exception {}".format(err))
            db_conn.rollback()
            cursor.close()
            db_conn.close()
            return False

    def find_not_read_message(self, to_user):
        db_conn = sqlite3.connect(sqlite3_host)
        cursor = db_conn.cursor()
        try:
            sql = f"""select * from message where status={MessageStatus.FAILED.value} and to_user_id={to_user};"""
            print(f"sql_statement: {sql}")
            cursor.execute(sql)
            ret = cursor.fetchall()
            print("ret: {}".format(ret))
            cursor.close()
            db_conn.close()
            return ret
        except Exception as err:
            print("user_is_valid: Exception {}".format(err))
            cursor.close()
            db_conn.close()
            return None

    def update_message_status(self, message_id):
        db_conn = sqlite3.connect(sqlite3_host)
        cursor = db_conn.cursor()
        try:
            sql = f"""update message set status={MessageStatus.SUCCESS.value}, send_time='{datetime.datetime.now()}'  where id={message_id};"""
            print(f"sql_statement: {sql}")
            cursor.execute(sql)
            db_conn.commit()
            cursor.close()
            db_conn.close()
            return True
        except Exception as err:
            print("user_is_valid: Exception {}".format(err))
            db_conn.rollback()
            cursor.close()
            db_conn.close()
            return False

    def get_user_name_by_id(self, user_id):
        db_conn = sqlite3.connect(sqlite3_host)
        cursor = db_conn.cursor()
        try:
            sql = f"""select user_name from user where id={user_id};"""
            print(f"sql_statement: {sql}")
            cursor.execute(sql)
            ret = cursor.fetchone()
            cursor.close()
            db_conn.close()
            return ret
        except Exception as err:
            print("get_user_name_by_id: Exception {}".format(err))
            cursor.close()
            db_conn.close()

    def send_no_read_message(self, to_user):
        all_not_read_message = self.find_not_read_message(to_user)
        for msg in all_not_read_message:
            from_user_name = self.get_user_name_by_id(msg[1])[0]
            message = {
                "from": from_user_name,
                "to": msg[2],
                "message": msg[3]
            }
            self.write_message(message)
            self.update_message_status(msg[0])
