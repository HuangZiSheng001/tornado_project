# coding:utf-8
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import json
import time
from tornado.options import define, options
from tornado.web import RequestHandler, authenticated

from tornado.websocket import WebSocketHandler


# tornado没有内置session
from pycket.session import SessionMixin


from data import connect
from data import user_modules

import util.ui_methods
import util.ui_modules

# from data import connect
# from data import user_modules




define('port', default=8080, help='run port', type=int)



class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('index')
        # self.set_cookie('cookie_test', 'aowuaowu')
        # self.set_cookie('cookie_test2', 'aowu', expires=time.time() + 60)
        # self.set_cookie('cookie_test3', 'aowuaowu', expires_days=2)
        # self.set_cookie('cookie_test4', 'aowu', httponly=True)
        # self.set_cookie('cookie_test5', 'aowu', max_age=120, expires=time.time())
        # self.set_secure_cookie('cookie_test7','aowuaowi')
        # self.render('08websocket.html')

    def post(self, *args, **kwargs):
        pass




class GetHandler(tornado.web.RequestHandler):
    def get(self):
        self.get_secure_cookie('cookie_test5')
        self.get_cookie('cookie_test7')




class BaseHandler(RequestHandler, SessionMixin):
    def get_current_user(self):
        current_user = self.session.get('user_ID')
        if current_user:
            return current_user

        return None



# 声明websocket基类
class BaseWebSocketHandler(WebSocketHandler, SessionMixin):
    def get_current_user(self):
        current_user = self.session.get('user_ID')
        if current_user:
            return current_user

        return None


# 聊天类
class ChatHandler(BaseWebSocketHandler):
    @authenticated
    def get(self):
        self.render('08websocket.html')

    def post(self):
        pass


#
class BuyHandler(BaseWebSocketHandler):
    @authenticated
    def get(self):
        self.write('黄梓晟同学买了很多东西')
        # 第一，这个参数如果有肯定是没登录的时候
        # 没登录，会跳转到login
        # 在login里面，form表单没提交之前，get里面获取一下这个值
        # 获取出来后，我们把这个值传到post请求里面
        # post获取这个值，此值就是一个url
        # 直接跳转此url



class LoginHandler(BaseWebSocketHandler):
    def get(self):
        next_name = self.get_argument('next', '')
        self.render(
            'in_out.html',
            nextname=next_name
        )


    def post(self):
        # 验证逻辑
        user = self.get_argument('name', None)
        password = self.get_argument('password', None)
        user_name = connect.session.query(user_modules.User.username == user).filter(
            user_modules.User.password == password).first()

        # 获取之前访问的路由
        next_name = self.get_argument('next', '')
        if user_name:
            # 设置加密cookie，保持登录状态
            # self.set_secure_cookie('user_ID', user)

            self.session.set('user_ID', user)
            self.redirect(next_name)
        else:
            self.write('账户信息错误，请核对')



class MessageHandler(BaseWebSocketHandler):
    # 建立连接，收发数据，断开连接

    users = set()

    # 建立连接完成的代码逻辑
    def open(self, *args, **kwargs):
        MessageHandler.users.add(self)
        # 服务器要告诉每一个客户端有人上线了
        for i in self.users:
            i.write_message('{}-上线了'.format(self.current_user))


    # 收发数据的代码逻辑
    def on_message(self, message):
        print(message)
        for i in self.users:
            i.write_message('{}说：{}'.format(self.current_user, message))


    def on_close(self):
        MessageHandler.users.remove(self)
        for i in self.users:
            i.write_message('{}-下线了'.format(self.current_user))



# 配置参数项
application = tornado.web.Application(
    handlers=[
        (r'/', IndexHandler),
        (r'/login', LoginHandler),
        (r'/buy', BuyHandler),
        (r'/websocket', MessageHandler),
        (r'/chat', ChatHandler),
    ],

    template_path='./templates',
    # 方便调试
    debug=True,
    static_path='./static',
    ui_methods=util.ui_methods,
    ui_modules=util.ui_modules,
    autoreload=None,     # 所有路由都取消转义
    cookie_secret='qwe123',  # 加盐
    login_url='/login',     # 登录的路由

    # 数据库配置
    pycket={
        'engine': 'redis',
        'storage': {
            'host': 'localhost',
            'port': '6379',
            'db_sessions': '5',
            'max_connections': 2**10,
        },
        'cookies': {
            'expires_days': 7,
        }
    }


)



if __name__ == "__main__":

    print('get to: http://127.0.0.1:8080')

    # 打印请求信息（日志信息）
    tornado.options.parse_command_line()

    http_serbver = tornado.httpserver.HTTPServer(application)

    # 绑定端口，主动变为被动
    http_serbver.listen(options.port)

    # 开启监听事件
    tornado.ioloop.IOLoop.current().start()

