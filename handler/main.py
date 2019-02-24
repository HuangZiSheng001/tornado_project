import os

from tornado.web import RequestHandler

from util.photo import get_imgs, save_thumbnail, get_thumbnail


# 主页面
class IndexHandler(RequestHandler):
    def get(self):
        images = get_imgs()

        self.render(
            template_name='index.html',
            images=images,
        )


# 发现最新上传图片的页面， 展示略缩图
class ExploreHandler(RequestHandler):
    def get(self):
        images = get_thumbnail()

        self.render(
            template_name='explore.html',
            images=images,
        )


# 用户详情页面， 展示完全图
class PostHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render(
            template_name='post.html',
            post_id=kwargs['post_id'],
        )


# 用户上传文件页面
class UploadHandler(RequestHandler):
    def get(self):
        self.render('upload.html')

    def post(self):
        img_list = self.request.files.get('picture', [])
        upload_img = img_list[0]

        # {"filename":..., "content_type":..., "body":...}
        # html content type对照表

        save_pic_path = os.path.join('./static/upload', upload_img['filename'])

        with open(save_pic_path, 'wb') as fp:
            fp.write(upload_img['body'])

        self.write('上传图片成功<hr>')

        save_thumbnail(image_path=save_pic_path)
        self.write('略缩图保存成功')




        # f''   python3.6  f string方法

        # self.write(upload_img['filename'] + ' ' + upload_img['content_type'])
        # self.write(save_pic_path)
