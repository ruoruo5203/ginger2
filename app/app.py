"""
 flask核心对象初始化
"""
# 重命名
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from app.libs.error_code import ServerError
from datetime import date


# 类对象josnf
class JSONEncoder(_JSONEncoder):
    def default(self, o):
        # 容错：客户端不能解决的问题就不要用
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        # 遇到不能序列化的会递归调用，需要考虑时间
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerError()

# 自定义flask核心对象，继承原来的flask，替换jsonencoder.
class Flask(_Flask):
    json_encoder = JSONEncoder



