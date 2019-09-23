"""

"""
from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db, MixinJSONSerializer
import datetime

__author__ = '七月'


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    auth = Column(SmallInteger, default=1)
    _password = Column('password', String(100))

    # key设定返回的属性（个性化），统一的重构到base里面。josnfiy
    def keys(self):
        return ['id', 'email', 'nickname', 'auth']

    # 某些属性设置为方法
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(nickname, account, secret):
        with db.auto_commit():
            # 在一个对象内部创建一个对象本身，使用静态方法或者类方法
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)


    #token需要调用，方法
    @staticmethod
    def verify(email, password):
        # 查询并访问用户
        user = User.query.filter_by(email=email).first_or_404()
        # 判断是否存在user，否则抛出异常，定义在error_code
        if not user.check_password(password):
            # 授权失败401
            raise AuthFailed()
        # 在model设置参数，token调用，生成token。读取，写入g变量，获得是否
        # 显示返回权限
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        # 返回UID
        return {'uid': user.id, 'scope': scope}

    # 检查密码
    def check_password(self, raw):
        if not self._password:
            return False
        # 密码加密hash密码
        return check_password_hash(self._password, raw)

    # def _set_fields(self):
    #     # self._exclude = ['_password']
    #     self._fields = ['_password', 'nickname']
