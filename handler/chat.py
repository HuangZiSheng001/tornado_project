import tornado
import uuid
import datetime

from tornado.httpclient import AsyncHTTPClient
from tornado.web import RequestHandler, authenticated
from tornado.ioloop import IOLoop

from .auth import AuthBaseWebSocketHandler
from util.auth import get_username_by_telephone


class MessageHandler(AuthBaseWebSocketHandler):
    """
    建立连接，收发数据，断开连接

    """
    # 用户列表
    users = set()

    # 传递历史消息
    history = []

    # 历史记录的大小
    history_size = 5

    def open(self, *args, **kwargs):
        """
        建立连接完成的代码逻辑
        :param args:
        :param kwargs:
        :return:
        """
        print("WebSocket opened {}".format(self))
        MessageHandler.users.add(self)
        for w in MessageHandler.users:
            w.write_message("{}--进入了聊天室".format(get_username_by_telephone(self.current_user)))

    def on_message(self, message):
        """
        收发数据的代码逻辑
        :param message:
        :return:
        """
        # print("get : {}".format(message))
        parsed = tornado.web.escape.json_decode(message)
        body = parsed['body']

        if body and (body.startswith("http://") or body.startswith("https://")):

            client = AsyncHTTPClient()

            # 拼接请求接口url
            save_api_url = "http://{ip}:{port}/save?save_url={save_url}&telephone={phone}&from=room".format(
                ip="127.0.0.1",
                port="8080",
                save_url=body,
                phone=self.current_user,
            )

            IOLoop.current().spawn_callback(client.fetch, save_api_url)

            chat = MessageHandler.make_chat(msg_body='picture link: {} is downloading...'.format(body))

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

        else:
            chat = MessageHandler.make_chat(
                name=get_username_by_telephone(self.current_user),
                msg_body=parsed['body'],
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

    @classmethod
    def make_chat(cls, msg_body, name='systerm', img_url=None):
        """
        生成chat
        :param msg_body:
        :param name:
        :param img_url:
        :return: chat 字典形式
        """
        chat = {
            'id': str(uuid.uuid4()),
            'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user': name,
            'body': msg_body,
            'img_url': img_url,
        }
        return chat

    @classmethod
    def update_history(cls, msg):
        """
        更新历史消息列表
        :param msg:
        :return:
        """
        MessageHandler.history.append(msg)

        # 截取历史记录
        if len(MessageHandler.history) > MessageHandler.history_size:
            MessageHandler.history = MessageHandler.history[-MessageHandler.history_size:]

    @classmethod
    def send_updates(cls, msg):
        """
        给每个等待接收的用户发新的消息
        :param msg:
        :return:
        """
        for w in MessageHandler.users:
            w.write_message(msg)

    def on_close(self):
        MessageHandler.users.remove(self)
        for i in self.users:
            i.write_message('{}--退出了聊天室'.format(get_username_by_telephone(self.current_user)))


class ChatRoomHandler(AuthBaseWebSocketHandler):
    """
    聊天类
    """
    @authenticated
    def get(self, *args, **kwargs):
        self.render(
            template_name='room.html',
            messages=MessageHandler.history,
            user=get_username_by_telephone(self.current_user),
        )

    def post(self):
        pass
