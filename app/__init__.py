"""
经常改动
"""
from .app import Flask



def register_blueprints(app):
    # 蓝图注册。先导入蓝图，再用app对蓝图进行注册
    from app.api.v1 import create_blueprint_v1
    # url_prefix可以指定url前缀
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_plugin(app):
    from app.models.base import db
    # 插件注册
    db.init_app(app)
    with app.app_context():
        # 必须在上下文环境中
        db.create_all()


def create_app():
    # 创建核心对象，指定位置信息，使用———name
    app = Flask(__name__)
    # 文件装在到核心对象中
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    #调用完成蓝图注册
    register_blueprints(app)
    # 定义后调用函数
    register_plugin(app)

    return app

