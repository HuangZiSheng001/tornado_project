# coding:utf-8
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import json
import time
from tornado.options import define, options


# from util import ui_methods
# from util import ui_modules

from data import connect
from data import user_modules




define('port', default=8080, help='run port', type=int)


class IndexHandler(tornado.web.RequestHandler):
    """
          主路由处理类
          访问网站根路径的时候实现的代码逻辑

    """
    def get(self):
        """
            对应http的get请求方式
        """
        self.write("Hello Itcast!")
        self.write('<br/>')
        self.write('Life is short You need python')

        # 刷新
        self.flush()
        my_di = {
            'name': 'hzs',
            'age': 19
        }
        self.write(my_di)
        my_li = ['hzs', 19]
        self.write(json.dump(my_li))
        self.finish()
        self.write('hahahahahahha')


# 获取get参数
class IndexHander_01(tornado.web.RequestHandler):
    def get(self):
        # 获取页面传过来的参数
        name_01 = self.get_argument('name', '?')
        # print(name_01)
        self.write(name_01 + ' , Welcome to my tornado server.<br>')

        name_02 = self.get_arguments('name')

        self.write('<br>self.get_arguments:<br>')
        for name in name_02:
            self.write(name + '<br>')


# render网页
class IndexHander_02(tornado.web.RequestHandler):
    def get(self):
        self.render('t_01.html')


# 路由跳转  重定向
class IndexHander_03(tornado.web.RequestHandler):
    def get(self):
        time.sleep(5)
        self.redirect('/python')


# 获取请求信息
class IndexHander_04(tornado.web.RequestHandler):
    def get(self):
        print(self.request)
        print(self.request.remote_ip)
        self.write(self.request.remote_ip)


# 取得post 的参数
class IndexHander_05(tornado.web.RequestHandler):
    def get(self):
        self.render('in_out.html')

    def post(self):
        name = self.get_argument('name', '')
        password = self.get_argument('password', '')
        self.write('用户名：' + name + '<br>')
        self.write('密码：' + password)


# 尝试用户登录  表单提交后，进入post方法
class IndexHander_06(tornado.web.RequestHandler):
    def get(self):
        self.write('hello world')

    def post(self):
        url_list = [
            ('https://www.baidu.com', '百度一下，你就知道'),
            ('https://www.zhihu.com', '知乎，分享你刚编的故事'),
            ('https://www.taobao.com', '上淘宝，就购了'),
        ]
        name = self.get_argument('name', '')
        # self.write(name)

        # 直接传进去会被转义    {% raw xxx %}  取消转义
        atga = """
            <a href="https://www.baidu.com" target="_blank">百度一下，你就知道</a>
        """

        self.render(
            'template_01.html',
            username=name,
            time=time.ctime(),
            url_list=url_list,
            atga=atga,
        )


# 转义
class IndexHander_07(tornado.web.RequestHandler):
    def get(self):
        # 直接传进去会被转义    {% raw xxx %}  取消转义
        atga = """
                    <a href="https://www.baidu.com" target="_blank">百度一下，你就知道</a>
                """
        self.render(
            'template_02.html',
            atga=atga,
        )

    def post(self):
        # 直接传进去会被转义    {% raw xxx %}  取消转义
        atga = """
            <a href="https://www.baidu.com" target="_blank">百度一下，你就知道</a>
        """
        self.render(
            'template_02.html',
            atga=atga,
        )



# 静态文件引入test
class IndexHander_08(tornado.web.RequestHandler):
    def get(self):
        self.render(template_name='login_02.html')

    def post(self):
        pass



class IndexHander_09(tornado.web.RequestHandler):
    def get(self):
        self.write('这是get方法')

    def post(self):
        name = self.get_argument('name', '')
        self.render(
            template_name='template_03.html',
            username=name,
                    )


# 传参的test
class SubHander_01(tornado.web.RequestHandler):
    def get(self, name, age):
        self.write(
            'name: {} <br />'.format(name) +
            'age: {} <br />'.format(age)
        )

    def post(self):
        pass


# 设置响应头test
class ResponseHander_01(tornado.web.RequestHandler):
    def get(self):
        # 可以设置多个，遇到相同时则喜新厌旧
        self.set_header('name', 'hzs')
        self.set_header('age', '111')

        # 可存在多个相同key
        self.add_header('name', 'jzy')

        # 清除响应头，名字符合的全部清除
        self.clear_header('age')


        # self.set_cookie()

    def post(self):
        pass


# 报错处理
class ErrorHander_01(tornado.web.RequestHandler):
    def get(self):
        self.write('this is my route')
        self.flush()

        # 状态码已经200后，不能再变成404了
        self.send_error(404)

    def write_error(self, status_code, **kwargs):
        # self.write('statu code: {}'.format(status_code))
        self.render(template_name='404.html')

    def post(self):
        pass



class NoneHandle_01(tornado.web.RequestHandler):
    def get(self, *args):
        self.send_error(404)
        # self.set_status(404, 'error!!!')

    def write_error(self, status_code, **kwargs):
        # self.write('statu code: {}'.format(status_code))
        self.render(template_name='404.html')

    def post(self):
        pass


# 客户端发送请求过来，我们发送响应头回去， 这一流程
class WorkHandle_01(tornado.web.RequestHandler):

    # 设置默认响应头
    def set_default_headers(self):
        print('-----set_default_headers------: 设置headers')

    # 初始化工作
    def initialize(self):
        print('---initialize----: 初始化')

    # 准备工作
    def prepare(self):
        print('---准备工作---')

    # get
    def get(self):
        self.write('haha  <br />  hzs ')

    # post
    def post(self):
        pass

    # 错误处理，发生错误时才调用
    def write_error(self, status_code, **kwargs):
        print('---错误处理---： 错误处理')

    # 结束工作
    def on_finish(self):
        print('---on finish---: 结束处理工作，释放资源')


# 继承
class InheritHandle_01(tornado.web.RequestHandler):

    def my_haha(self):
        return 'haha'

    def get(self):
        self.render(template_name='template_04.html')


    def post(self, *args, **kwargs):
        pass


# 自己定义的类
class MyClass_01(object):
    def func_01(self):
        return 'this is my func_01'

    def __call__(self, *args, **kwargs):
        return 'this is call '


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('in_out.html')

    def post(self):
        # 验证逻辑
        user = self.get_argument('name', None)
        password = self.get_argument('password', None)
        user_name = connect.session.query(user_modules.User.username == user).filter(user_modules.User.password == password).first()
        if user_name :
            self.render(
                template_name='template_03.html',
                username=user,
            )
        else:
            self.write('账户信息错误，请核对')




# 配置参数项
application = tornado.web.Application(
    handlers=[
        (r'/', IndexHandler),
        (r'/index', IndexHander_01),
        (r'/python', IndexHander_02),
        (r'/python_01', IndexHander_03),
        (r'/ip', IndexHander_04),
        (r'/post', IndexHander_05),
        (r'/login_01', IndexHander_05),
        (r'/login_ok_01', IndexHander_06),
        (r'/zhuanyi_01', IndexHander_07),
        (r'/login_02', IndexHander_08),
        (r'/login_ok_02', IndexHander_09),
        (r'/sub_01/(?P<name>.+)/(?P<age>[0-9]+)', SubHander_01),
        (r'/response_01', ResponseHander_01),
        (r'/error_01', ErrorHander_01),
        (r'/work_01', WorkHandle_01),
        (r'/inhert_01', InheritHandle_01),

        (r'/login_ok_03', LoginHandler),

        # 接受找不到的路由
        (r'/(.*)', NoneHandle_01),

    ],

    template_path='./templates',
    # 方便调试
    debug=True,
    static_path='./static',
    # ui_methods=util.ui_methods,
    # ui_modules=util.ui_modules,
    # autoreload=None,     # 所有路由都取消转义
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

