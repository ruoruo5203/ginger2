"""

"""
from collections import namedtuple

from flask import current_app, g, request
# 编写装饰器
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope


# 实例化。httpbasicahth是一个对象，账号密码，必须放在头中发送key:value.
# 设定一个固定的authorization：base64加密
# key：authorization，value:basic base64加密(账号：密码）
auth = HTTPBasicAuth()
# 对象式结构
User = namedtuple('User', ['uid', 'ac_type', 'scope'])


@auth.verify_password
def verify_password(token, password):
    # 为什么authorization传递token就可以传递token？？？
    # token
    # HTTP 账号密码
    # header key:value
    # account  qiyue
    # 123456
    # key=Authorization
    # value =basic base64(qiyue:123456)
    # 实例化
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        # request。设置一个g变量？？保存。类似代理模式
        g.user = user_info
        return True


def verify_auth_token(token):
    # 实例化序列化器
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        # 解密
        data = s.loads(token)
    #     是否合法，捕捉特定异常
    except BadSignature:
        raise AuthFailed(msg='token is invalid',
                         error_code=1002)
    # 是否过期，捕捉特定异常
    except SignatureExpired:
        raise AuthFailed(msg='token is expired',
                         error_code=1003)
    # 读取数据，字典形式
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    # request 视图函数.判断对应的权限和视图函数
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    # 返回信息，实例化，优势？
    return User(uid, ac_type, scope)
