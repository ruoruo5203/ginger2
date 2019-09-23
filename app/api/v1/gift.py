"""
 Created by 七月 on 2018/5/28.
"""
from flask import g

from app.libs.error_code import Success, DuplicateGift
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.book import Book
from app.models.gift import Gift



api = Redprint('gift')


@api.route('/<isbn>', methods=['POST'])
@auth.login_required
def create(isbn):
    # 拿到id号
    uid = g.user.uid
    with db.auto_commit():
        # 判断是否存在
        Book.query.filter_by(isbn=isbn).first_or_404()
        # 是否已经赠送
        gift = Gift.query.filter_by(isbn=isbn, uid=uid).first()
        if gift:
            raise DuplicateGift()
        gift = Gift()
        gift.isbn = isbn
        gift.uid = uid
        db.session.add(gift)
    return Success()




