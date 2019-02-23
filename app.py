import tornado.ioloop
import tornado.web
import tornado.options


from tornado.options import define, options
from tornado.web import RequestHandler


define('port', default=8080, help='listening port', type=int)


# 主页面
class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html')



# 发现最新上传图片的页面
class ExploreHandler(RequestHandler):
    def get(self):
        self.render('explore.html')


# 用户详情页面
class PostHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render(
            template_name='post.html',
            post_id=kwargs['post_id'],
        )


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/explore', ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)', PostHandler),
        ]
        settings = dict(
            debug=True,
            template_path='./templates',
            static_path='./static',
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

