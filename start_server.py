
import tornado.ioloop
import tornado.web

from web_handler.router import router

settings = {
    "login_url": "/login",
    "cookie_secret": "MeChat-2149c62a-8261-4250-88cd-9900dd075c63"
}

if __name__ == "__main__":
    app = tornado.web.Application(
        router,
        **settings
    )
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()