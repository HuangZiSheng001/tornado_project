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


# 用户提交
class UploadHandler(RequestHandler):
    def get(self):
        self.render('upload.html')

    def post(self):
        img_list = self.request.file.get('picture', [])
        upload_img = img_list[0]

        # {"filename":..., "content_type":..., "body":...}
        # html content type对照表
        with open(upload_img['filename'], 'wb') as fp:
            fp.write(upload_img['body'])
            pass

        self.write(upload_img['filename'] + ' ' + upload_img['content_type'])
