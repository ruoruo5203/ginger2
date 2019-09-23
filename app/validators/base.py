"""
 Created by 七月 on 2018/5/12.
"""
from flask import request
from wtforms import Form

from app.libs.error_code import ParameterException



# 改写wtforms，自己创建全部校验抛出异常
class BaseForm(Form):
    def __init__(self):
        # 通过json获取参数。如果指定了content_type指的是body里面的参数,尝试反序列化body为空，不要报错（silent)
        data = request.get_json(silent=True)
        # 查询参数的获取
        args = request.args.to_dict()
        # 参数传递进去，**args
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            # form error_code,通过传递msg
            raise ParameterException(msg=self.errors)
        return self
