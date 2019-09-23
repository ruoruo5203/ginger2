"""
 Created by 七月 on 2018/5/8.
"""
from sqlalchemy import or_

from app.libs.redprint import Redprint
from app.models.book import Book
from app.validators.forms import BookSearchForm
from flask import jsonify

# 实例化红图对象
api = Redprint('book')

# 如何接受q查询参数。参数一定要验证，在forms里面进行验证
# 在base里面通过request。json拿到参数
@api.route('/search')
def search():
    # 实例化，然后调用
    form = BookSearchForm().validate_for_api()
    # 获取q。模糊搜索前后+%
    q = '%' + form.q.data + '%'
    #
    # sqlalchey实例化变量，不是通过普通的， book = Book()。而是通过元类 ORM创建的，，在ssqlalchey里面，不会去执行构造函数，使用装饰器
    # 模糊查询sqlalchemy方法。or_意思是或关系，默认是且关系。需要导入
    books = Book.query.filter(
        or_(Book.title.like(q), Book.publisher.like(q))).all()
    # 去除掉某些字段的返回，比如summary。hide方法。在book下面新建hide方法
    books = [book.hide('summary') for book in books]
    return jsonify(books)

# 搜索后进入详情页，简单检索
@api.route('/<isbn>/detail')
def detail(isbn):
    book = Book.query.filter_by(isbn=isbn).first_or_404()
    return jsonify(book)
