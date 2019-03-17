import requests

from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient

from .main import AuthBaseHandler
from util.photo import UploadImage, add_post_for


class SyncSaveHandler(AuthBaseHandler):
    """
    同步版本的保存URL
    """
    def get(self, *args, **kwargs):
        save_url = self.get_argument('save_url', None)

        resp = requests.get(save_url)
        uim = UploadImage(old_name='x.jpg', static_path=self.settings['static_path'])
        uim.save_upload_pic(resp.content)
        uim.save_thumbnail()

        post = add_post_for(
            telephone=self.current_user,
            image_url=uim.upload_img_url,
            thumb_url=uim.thumb_url,
        )

        self.redirect('/post/{}'.format(post.id))


class AsyncSaveHandler(AuthBaseHandler):
    """
    异步版本保存url图片
    应做成API效果
    """
    @coroutine
    def get(self, *args, **kwargs):
        save_url = self.get_argument('save_url', None)

        resp = yield self.get_resp(save_url)

        uim = UploadImage(old_name='x.jpg', static_path=self.settings['static_path'])

        uim.save_upload_pic(resp.body)

        uim.save_thumbnail()

        post = add_post_for(
            telephone=self.current_user,
            image_url=uim.upload_img_url,
            thumb_url=uim.thumb_url,
        )

        self.redirect('/post/{}'.format(post.id))

    @coroutine
    def get_resp(self, url):
        client = AsyncHTTPClient()
        resp = yield client.fetch(url, connect_timeout=30, request_timeout=50)
        return resp
