"""
 Created by 七月 on 2018/5/8.
"""
from flask import jsonify, g

from app.libs.error_code import DeleteSuccess, AuthFailed
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User

__author__ = '七月'
# 实例化红图
api = Redprint('user')


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    # 类变量无法使用__dict__（对象转字典）进行，实例变量变成dict
    # 对象不可以用[]方法访问，但是为其增加方法就可以__getitem__   getattr拿到对应属性值
    # get_or_404会返回所有的数据
    # fifter_by后面写具体的。查询大于多少的用fifter
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)

# 视图函数，装饰器，传入url
@api.route('', methods=['GET'])
# 验证令牌是否合法，是否过期
@auth.login_required
def get_user():
    # 传递参数
    uid = g.user.id
    # 获取用户ID。需要重写fist_or_404,自带的返回格式不是josn的
    # 本身无法直接。如何能够序列化。如果是字典，直接序列化，如果不是，去defalut函数查找。这里需要default重写（继承，覆盖）
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


# 管理员
@api.route('/<int:uid>', methods=['DELETE'])
# 管理员，超权行为
def super_delete_user(uid):
    pass

# 带/重定向
@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    # 不从用户参数 获得uid，避免超权，从token获得。但是管理员就要有超权行为
    # nametuple,key用字典访问
    # g变量线程隔离，不会出现数据错乱问题
    uid = g.user.uid
    with db.auto_commit():
        # 首选查询，然后删除(定义在base里面）
        # query,filter_by已经该写过，查询states状态为0的
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()


@api.route('', methods=['PUT'])
def update_user():
    return 'update qiyue'


