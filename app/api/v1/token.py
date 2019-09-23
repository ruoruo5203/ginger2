"""
 Created by 七月 on 2018/5/13.
"""
from flask import current_app, jsonify

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import AuthFailed
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, TokenForm
# 令牌加密算法，改名
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, \
    BadSignature
# 实例化红图对象
api = Redprint('token')


# 登录，post传递参数相对而言比较安全
@api.route('', methods=['POST'])
def get_token():
    # 实例化然后构建form验证器
    form = ClientForm().validate_for_api()
    # 区分不同客户端类型，执行user.verify静态方法
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify,
    }
    # 获取用户ID号
    identity = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )
    # Token，首先传入过期时间。开发阶段比较长。上线后，修改短一点。
    expiration = current_app.config['TOKEN_EXPIRATION']
    # 从字典中取出UID，客户端类型，过期时间。token只是字符串
    token = generate_auth_token(identity['uid'],
                                form.type.data,
                                identity['scope'],
                                expiration)
    # token令牌生成的字符串是？？需要调用decode修改成普通字符串
    t = {
        'token': token.decode('ascii')
    }
    # 返回t，序列号，以及状态码
    return jsonify(t), 201


@api.route('/secret', methods=['POST'])
def get_token_info():
    """获取令牌信息"""
    # 验证参数
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    # 判断合法
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)

    r = {
        'scope': data[0]['scope'],
        # 创建时间
        'create_at': data[1]['iat'],
        # 有效期
        'expire_in': data[1]['exp'],
        'uid': data[0]['uid']
    }
    return jsonify(r)


def generate_auth_token(uid, ac_type, scope=None,
                        expiration=7200):
    """生成令牌，加密，并且写入信息。UID，客户端类型，权限作用域，过期时间"""
    # 实例化一个序列化器，已改名。传递钥匙，令牌有效期
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    #dumps方法以字典形式写入进去令牌，最终返回字符串，也就是令牌
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope':scope
    })
