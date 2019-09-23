"""

"""
from app.libs.error_code import NotFound



"""

"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import inspect, Column, Integer, SmallInteger, orm
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            # Session类似链接
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)
    # 重写json格式返回
    def get_or_404(self, ident):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv
    # 重构json格式返回
    def first_or_404(self):
        rv = self.first()
        if not rv:
            raise NotFound()
        return rv

# 链接数据库
db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    # 和keys对应使用，jsonify
    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.status = 0


    def keys(self):
        return self.fields
    # 所有模型都需要隐藏字段模型
    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self







# 自己写的一个序列化器，不需要keys
class MixinJSONSerializer:
    @orm.reconstructor
    def init_on_load(self):
        self._fields = []
        # self._include = []
        self._exclude = []

        self._set_fields()
        self.__prune_fields()

    def _set_fields(self):
        pass

    def __prune_fields(self):
        columns = inspect(self.__class__).columns
        if not self._fields:
            all_columns = set(columns.keys())
            self._fields = list(all_columns - set(self._exclude))

    def hide(self, *args):
        for key in args:
            self._fields.remove(key)
        return self

    def keys(self):
        return self._fields

    def __getitem__(self, key):
        return getattr(self, key)
