import tornado
import uuid
import datetime
from util.auth import get_username_by_telephone

from tornado.web import RequestHandler, authenticated
from .auth import AuthBaseWebSocketHandler


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
            w.write_message(f"{get_username_by_telephone(self.current_user)}--进入了聊天室")

    def on_message(self, message):
        """
        收发数据的代码逻辑
        :param message:
        :return:
        """
        print(f"get : {message}")
        parsed = tornado.web.escape.json_decode(message)
        chat = {
            'id': str(uuid.uuid4()),
            'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user': get_username_by_telephone(self.current_user),
            'body': parsed['body'],
        }
        msg = {
            'html': tornado.web.escape.to_basestring(
                self.render_string(
                    template_name='message.html',
                    chat=chat,
                )
            ),
            'id': chat['id'],
        }
        MessageHandler.history.append(msg)

        # 截取历史记录
        if len(MessageHandler.history) > MessageHandler.history_size:
            MessageHandler.history = MessageHandler.history[-MessageHandler.history_size:]

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
