import tornado.web

from web_handler.base_handler import BaseHandler
from web_handler.status_const import Status


class LogOutHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        self.clear_all_cookies()
        return self.response_cli(Status.SUCCESS)
