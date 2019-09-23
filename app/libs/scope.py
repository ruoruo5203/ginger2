"""
判断是否可以访问api
"""




class Scope:
    allow_api = []
    allow_module = []
    # 模块名
    forbidden = []

    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))
        # 运算符重载，add变成__add_可以实现对象＋操作

        self.allow_module = self.allow_module + \
                            other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden = self.forbidden + other.forbidden
        # 去重
        self.forbidden = list(set(self.forbidden))

        return self


class AdminScope(Scope):
    # allow_api = ['v1.user+super_get_user',
    #              'v1.user+super_delete_user']
    # 实现视图函数下面所有函数
    allow_module = ['v1.user']

    def __init__(self):
        # 排除
        pass
        # self + UserScope()


class UserScope(Scope):
    allow_module = ['v1.gift']
    forbidden = ['v1.user+super_get_user',
                 'v1.user+super_delete_user']

    def __init__(self):
        self + AdminScope()
    #     api合并
    # allow_api = ['v1.user+get_user', 'v1.user+delete_user']


def is_in_scope(scope, endpoint):
    # scope()
    # 反射
    # globals
    # v1.view_func   v1.module_name+view_func
    # v1.red_name+view_func
    # 根据类的名字动态创建对象，globals可以把当前变量都变成字典，方法，调用，实例化
    scope = globals()[scope]()
    # 拿到v1
    splits = endpoint.split('+')
    # 拿到module
    red_name = splits[0]
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    # 判断模块
    if red_name in scope.allow_module:
        return True
    else:
        return False
