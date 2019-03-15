import tornado.ioloop
import tornado.web
import tornado.options


from tornado.options import define, options


# tornado没有内置session

from handler.auth import LoginHandler, LoginOutHandler, RegistHandler
from handler.main import IndexHandler, ExploreHandler, PostHandler, UploadHandler, NoneHandle_01
from handler.main import ProfileHandler
from handler.chat import MessageHandler, ChatRoomHandler

import util.ui_methods
import util.ui_modules


define('port', default=8080, help='listening port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/explore', ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)', PostHandler),
            (r'/upload', UploadHandler),
            (r'/login', LoginHandler),
            (r'/regist', RegistHandler),
            (r'/logout', LoginOutHandler),
            (r'/profile', ProfileHandler),

            (r'/ws', MessageHandler),
            (r'/chat', ChatRoomHandler),

            # 接受找不到的路由
            (r'/(.*)', NoneHandle_01),
        ]
        settings = dict(
            debug=True,
            template_path='./templates',
            static_path='./static',

            # 静态文件url前缀
            # static_url_prefix='/pic/',

            ui_methods=util.ui_methods,
            ui_modules=util.ui_modules,
            autoreload=None,                # 所有路由都取消转义
            cookie_secret='qwe123',         # 加盐
            login_url='/login',             # 登录的路由

            # 数据库配置
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    'port': '6379',
                    'db_sessions': '6',
                    'max_connections': 2 ** 10,
                },
                'cookies': {
                    'expires_days': 7,
                }
            }
        )

        super().__init__(handlers, **settings)



if __name__ == '__main__':
    # 初始化Application()
    application = Application()

    print('get to: http://127.0.0.1:8080')

    # 打印日志信息
    tornado.options.parse_command_line()

    application.listen(options.port)

    # 开启监听事件
    tornado.ioloop.IOLoop.current().start()

