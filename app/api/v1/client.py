"""
 Created by 七月 on 2018/5/10.
"""
from flask import request, jsonify

from app.libs.error_code import ClientTypeError, Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm
from app.libs.enums import ClientTypeEnum
from werkzeug.exceptions import HTTPException

__author__ = '七月'

api = Redprint('client')

# 所有参数都要从form里面获取，这样会进行一定的验证
@api.route('/register', methods=['POST'])
def create_client():
    # 实例化clientformd调用值validate进行校验
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    # 取枚举类型
    promise[form.type.data]()
    return Success()

# 总分关系
def __register_user_by_email():
    # 实例化useremailform.并且传递
    form = UserEmailForm().validate_for_api()
    # 读取参数
    User.register_by_email(form.nickname.data,
                           form.account.data,
                           form.secret.data)
