import time

from tornado.web import RequestHandler, authenticated
from util.photo import get_all_post, add_post_for, get_post_by_id, get_posts_for
from util.photo import UploadImage, get_like_count, get_like_posts
from .auth import AuthBaseHandler


# 主页面，所关注的用户的图片展示
class IndexHandler(AuthBaseHandler):

    def get(self):

        my_post = get_posts_for(self.current_user)

        self.render(
            template_name='index.html',
            posts=my_post,
            user=self.current_user,
        )


class ExploreHandler(AuthBaseHandler):
    """
    发现最新上传图片的页面， 展示略缩图, 需要登陆后才能访问
    """
    @authenticated
    def get(self):
        page = int(self.get_argument('page', '1'))
        posts = get_all_post(page=page)
        self.render(
            template_name='explore.html',
            posts=posts,
            user=self.current_user,
        )


class PostHandler(AuthBaseHandler):
    """
    用户详情页面， 展示完全图, 需要登陆后才能访问
    """
    @authenticated
    def get(self, *args, **kwargs):
        like_count = 3
        self.render(
            template_name='post.html',
            post=get_post_by_id(kwargs['post_id']),
            user=self.current_user,
            like_count=like_count,
        )


class UploadHandler(AuthBaseHandler):
    """
    用户上传文件页面, 需要登陆后才能访问
    """
    @authenticated
    def get(self, *args, **kwargs):
        self.render(
            template_name='upload.html',
            user=self.current_user,
        )

    def post(self, *args, **kwargs):

        img_list = self.request.files.get('picture', ['static_path'])

        post_id = 0

        for upload_img in img_list:

            my_upload_image = UploadImage(old_name=upload_img['filename'], static_path=self.settings['static_path'])

            my_upload_image.save_upload_pic(upload_img['body'])

            my_upload_image.save_thumbnail()

            post = add_post_for(self.current_user, my_upload_image.upload_img_url, my_upload_image.thumb_url)

            post_id = post.id

        self.redirect(f'/post/{post_id}')


class ProfileHandler(AuthBaseHandler):
    """
    用户信息中心
    """
    def get(self, *args, **kwargs):
        user_id = self.get_argument('user_id', '')
        if not user_id:
            telephone = self.current_user
        else:
            # 通过user_id 拿到telephone
            telephone = 0

        posts = get_posts_for(user_phone=self.current_user)
        like_posts = get_like_posts(telephone=telephone)

        self.render(
            template_name='profile.html',
            posts=posts,
            like_posts=like_posts,
        )





# 接收找不到的路由
class NoneHandle_01(RequestHandler):
    def get(self, *args):
        self.send_error(404)
        # self.set_status(404, 'error!!!')

    def write_error(self, status_code, **kwargs):
        # self.write('statu code: {}'.format(status_code))
        self.render(template_name='404.html')

    def post(self):
        pass


'''
     def post(self, *args, **kwargs):
         img_list = self.request.files.get('picture', [])

         post_id = 0

         for upload_img in img_list:

             upload_img_path = save_upload_pic(upload_img)

             thumb_path = save_thumbnail(image_path=upload_img_path)

             post = add_post_for(self.current_user, upload_img_path, thumb_path)

             post_id = post.id

         self.write('略缩图保存成功, 5秒后将跳转到详情页')

         time.sleep(5)

         self.redirect(f'/post/{post_id}')
     '''