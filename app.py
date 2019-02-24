import tornado.ioloop
import tornado.web
import tornado.options


from tornado.options import define, options


from handler.main import IndexHandler, ExploreHandler, PostHandler, UploadHandler


define('port', default=8080, help='listening port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/explore', ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)', PostHandler),
            (r'/upload', UploadHandler),
        ]
        settings = dict(
            debug=True,
            template_path='./templates',
            static_path='./static',
            # static_url_prefix='/pic/',
        )
        super().__init__(handlers, **settings)



if __name__ == '__main__':
    application = Application()

    print('get to: http://127.0.0.1:8080')

    # 打印日志信息
    tornado.options.parse_command_line()

    application.listen(options.port)

    # 开启监听事件
    tornado.ioloop.IOLoop.current().start()

