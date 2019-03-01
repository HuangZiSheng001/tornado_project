from tornado.web import RequestHandler, authenticated

from tornado.websocket import WebSocketHandler

# tornado没有内置session
from pycket.session import SessionMixin




class BaseHandler(RequestHandler, SessionMixin):
    def get_current_user(self):
        current_user = self.session.get('user_ID')
        if current_user:
            return current_user

        return None





# 声明websocket基类, 采用websocket协议
class BaseWebSocketHandler(WebSocketHandler, SessionMixin):
    def get_current_user(self):
        current_user = self.session.get('user_ID')
        if current_user:
            return current_user

        return None