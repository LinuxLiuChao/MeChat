from web_handler.chat_handler import ChatHandler
from web_handler.echo_handler import EchoHandler
from web_handler.login_handler import LoginHandler
from web_handler.logout_handler import LogOutHandler
from web_handler.main_handler import MainHandler

router = [
    (r"/", MainHandler),
    (r"/echo", EchoHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogOutHandler),
    (r"/chat", ChatHandler),

]
