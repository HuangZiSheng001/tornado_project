# - 认识路由

# - tornado启动

# python
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import define, options

define('port', default=9000, type=int, help='run port')



