


class HandlerProcess:
    def __init__(self):
        self.cookie = None
        self._handler = {
            "login": self.login,
            "logout": self.logout,
            "chat": self.chat
        }

    def login(self, *args):
        if len(args) != 3:
            print(f"params is wrong, usage: login <username> <password>\n")
            return
        _, user_name, password = args

        try:
            print(f"login {user_name}, {password}")
            pass
        except Exception as err:
            print(f"login Exception: {err}")

    def logout(self, *args):
        pass

    def chat(self, *args):
        pass

    def handler(self, *args):
        cmd = args[0]
        if cmd not in self._handler:
            print("Input command incorrect")
            return None
        return self._handler[cmd](*args)
