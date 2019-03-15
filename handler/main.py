import time

from tornado.web import RequestHandler, authenticated
from tornado.websocket import WebSocketHandler

from util.photo import get_all_post, add_post_for, get_post_by_id, get_posts_for
from util.photo import UploadImage, get_like_count, get_like_posts, make_page, mark_like
from util.auth import get_username_by_telephone
from .auth import AuthBaseHandler


class IndexHandler(AuthBaseHandler):
    """
    主页面
    """
    def get(self):

        my_post = get_posts_for(self.current_user)

        self.render(
            template_name='index.html',
            posts=my_post,
            user=get_username_by_telephone(telephone=self.current_user),
        )


class ExploreHandler(AuthBaseHandler):
    """
    发现最新上传图片的页面， 展示略缩图, 需要登陆后才能访问
    """
    @authenticated
    def get(self):
        page_number = int(self.get_argument('page', '1'))
        per_page = int(self.get_argument('number', '10'))
        pg = make_page(page=page_number, per_page=per_page)

        # posts = get_all_post(page=page)

        self.render(
            template_name='explore.html',
            # posts=posts,
            user=get_username_by_telephone(self.current_user),
            pg=pg,
            page_number=page_number,
        )


class PostHandler(AuthBaseHandler):
    """
    用户详情页面， 展示完全图, 需要登陆后才能访问
    """
    @authenticated
    def get(self, *args, **kwargs):
        like_count = get_like_count(kwargs['post_id'])
        self.render(
            template_name='post.html',
            post=get_post_by_id(kwargs['post_id']),
            user=get_username_by_telephone(self.current_user),
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
            user=get_username_by_telephone(self.current_user),
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
    @authenticated
    def get(self, *args, **kwargs):

        user_phone = self.get_argument('telephone', '')
        if not user_phone:
            user_phone = self.current_user

        posts = get_posts_for(user_phone=user_phone)
        like_posts = get_like_posts(telephone=user_phone)

        self.render(
            template_name='profile.html',
            posts=posts,
            like_posts=like_posts,
            user=get_username_by_telephone(self.current_user),
        )


class ChatHandle(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.render('room,html')





class NoneHandle_01(RequestHandler):
    """
    接收找不到的路由
    """
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