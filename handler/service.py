import requests
import uuid
import tornado.escape
import datetime
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient

from .chat import MessageHandler
from .main import AuthBaseHandler

from util.photo import UploadImage, add_post_for
from util.auth import get_username_by_telephone


class SyncSaveHandler(AuthBaseHandler):
    """
    同步版本的保存URL
    """
    def get(self, *args, **kwargs):
        save_url = self.get_argument('save_url', None)
        telephone = self.get_argument('telephone', self.current_user)

        resp = requests.get(save_url)
        uim = UploadImage(old_name='x.jpg', static_path=self.settings['static_path'])
        uim.save_upload_pic(resp.content)
        uim.save_thumbnail()

        post = add_post_for(
            telephone=telephone,
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
        telephone = self.get_argument('telephone', self.current_user)

        is_from_romm = self.get_argument('from', '') == 'room'

        if not is_from_romm:
            return

        resp = yield self.get_resp(save_url)

        uim = UploadImage(old_name='x.jpg', static_path=self.settings['static_path'])
        uim.save_upload_pic(resp.body)
        uim.save_thumbnail()

        post = add_post_for(
            telephone=telephone,
            image_url=uim.upload_img_url,
            thumb_url=uim.thumb_url,
        )

        chat = MessageHandler.make_chat(
            msg_body='{user} upload: http://{ip_port}/post/{post_id}'.format(
                ip_port="192.168.6.129:8080",
                user=get_username_by_telephone(telephone),
                post_id=post.id
            ),
            img_url=post.thumb_url,
        )

        msg = {
            'html': tornado.web.escape.to_basestring(
                self.render_string(
                    template_name='message.html',
                    chat=chat,
                )
            ),
            'id': chat['id'],
        }

        MessageHandler.update_history(msg)
        MessageHandler.send_updates(msg)

    @coroutine
    def get_resp(self, url):
        client = AsyncHTTPClient()
        resp = yield client.fetch(url, connect_timeout=30, request_timeout=50)
        return resp
