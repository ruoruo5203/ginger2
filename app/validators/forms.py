"""
 Created by 七月 on 2018/5/10.
"""
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp
from wtforms import ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form

__author__ = '七月'

# 类似于基类校验
class ClientForm(Form):
    # 传递一些自定义信息
    account = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=5, max=32
    )])
    secret = StringField()
    # 已经把数字转化为枚举类型
    type = IntegerField(validators=[DataRequired()])
    # 所有的代码都要进行校验，写在基类里面，就是运用面向对象的继承特性，减少代码量
    # 已经把数字转化为枚举类型
    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        # 把枚举转化给type
        self.type.data = client


class UserEmailForm(ClientForm):
    # 个性化form校验
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                        length(min=2, max=22)])

    def validate_account(self, value):
        # 查询数据库是否存在参数
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired()])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])
