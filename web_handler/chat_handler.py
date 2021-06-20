import json

from web_handler.base_handler import WsBaseHandler

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
            to_user_connect = connections.get(to_user)
            if not to_user_connect:
                print("to_user disOnline")
                self.write_message({"status": "failed", "text": "{} disOnline".format(to_user)})
            else:
                to_user_connect.write_message(message)
                print("send to {} success".format(to_user))

    def on_close(self):
        user_name = address.get(self.client_address)
        if user_name:
            connections.pop(user_name)
        print("websocket connection({}:{}) closed.".format(user_name, self.client_address))
