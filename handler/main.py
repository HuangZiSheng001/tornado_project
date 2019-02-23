from tornado.web import RequestHandler


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
