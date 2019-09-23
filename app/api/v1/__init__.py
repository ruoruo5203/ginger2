"""
 Created by 七月 on 2018/5/8.
"""
from flask import Blueprint
from app.api.v1 import user, book, client, token,gift




def create_blueprint_v1():
    # 实例化蓝图，第一个参数传递名称，第二个参数指定位置信息
    bp_v1 = Blueprint('v1', __name__)
    #
    user.api.register(bp_v1)
    book.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    gift.api.register(bp_v1)
    return bp_v1
