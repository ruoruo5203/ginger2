"""
 Created by 七月 on 2018/5/26.
"""
from sqlalchemy import Column, String, Integer, orm

from app.models.base import Base

__author__ = '七月'

# 定义一大堆数据。
class Book(Base):
    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 是否为空
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))


    # 定义keys方法，也就是默认输出字段
    # 装饰器，方便执行构造函数
    @orm.reconstructor
    def __init__(self):
        # 返回的是属性。这样就可以修改变量。如果fields是类变量，就会同时删除，所有只能定义为类变量
        self.fields = ['id', 'title', 'author', 'binding',
                       'publisher',
                       'price','pages', 'pubdate', 'isbn',
                       'summary',
                       'image']

