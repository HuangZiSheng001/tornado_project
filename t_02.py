# coding:utf-8
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import json
import time
import requests

from tornado.options import define, options
from tornado.web import RequestHandler, authenticated, asynchronous


from tornado.websocket import WebSocketHandler
from tornado.concurrent import run_on_executor

from concurrent.futures import ThreadPoolExecutor


# tornado没有内置session
from pycket.session import SessionMixin


from data import connect
from data import user_modules
from data.user_modules import User

import util.ui_methods
import util.ui_modules

# from data import connect
# from data import user_modules

define('port', default=8080, help='run port', type=int)


# 用这个handler来模仿我们实际的请求数据的一个接口
# 一般情况下为耗时的过程
class SyncHandler(RequestHandler):
    def get(self):
        self.write('--start--request--<br />')
        time.sleep(15)

        name = self.get_argument('name', '')
        self.write(name)
        self.write('--done--request---<br />')




class IndexHandler(RequestHandler):
    # 回调函数的异步操作
    @tornado.web.asynchronous
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()

        # fetch接受接口
        response = client.fetch('http://127.0.0.1:8080/sync', callback=self.on_response)

        self.write('ok')

    def on_response(self, res):
        # 回调函数打印请求数据
        self.write(str(res.body))
        self.finish()



class AsyncHandler(RequestHandler):
    @asynchronous
    def get(self):
        # http_client = AsyncHTTPClient()
        # http_client.fetch("http://example.com",
        #                  callback=self.on_fetch)
        pass

    def on_fetch(self, response):
        # do_something_with_response(response)
        # self.render("template.html")
        pass


class ABC(RequestHandler):
    def get(self):
        self.write('abc')

    def post(self):
        pass


class My_RequestHandler(RequestHandler):
    executor = ThreadPoolExecutor()

    # 协程装饰器
    @tornado.web.gen.coroutine
    def get(self):
        response = yield self.func()
        self.write(response.text)

    # coroutine 协同程序
    @tornado.web.gen.coroutine
    def func(self):
        res = requests.get('http://127.0.0.1:8080/sync?name=黄梓晟')
        return res



# 当前官方推荐版本
class GenHandler(RequestHandler):

    # 协程装饰器
    # @tornado.concurrent.run_on_executor
    @tornado.web.gen.coroutine
    def get(self):
        response = yield self.func()

        # 请求收到的数据
        self.write(response.body)

    @run_on_executor
    @tornado.web.gen.coroutine
    def func(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.web.gen.Task(client.fetch, 'http://127.0.0.1:8080/sync?name=hzs')

        # 返回数据出去
        raise tornado.web.gen.Return(response)



'''
@gen.coroutine
def get(self):
    http_client = AsyncHTTPClient()
    response1, response2 = yield [http_client.fetch(url1),
                                  http_client.fetch(url2)]
    response_dict = yield dict(response3=http_client.fetch(url3),
                               response4=http_client.fetch(url4))
    response3 = response_dict['response3']
    response4 = response_dict['response4']
'''

# 配置参数项
application = tornado.web.Application(
    handlers=[
        (r'/sync', SyncHandler),
        (r'/index', IndexHandler),
        (r'/abc', ABC),
        (r'/gen', GenHandler),
        (r'/req', My_RequestHandler),
    ],

    template_path='./templates',
    # 方便调试
    debug=True,
    static_path='./static',
    # ui_methods=util.ui_methods,
    # ui_modules=util.ui_modules,
    autoreload=None,     # 所有路由都取消转义

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

