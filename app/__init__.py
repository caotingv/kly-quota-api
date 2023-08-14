# __inint__.py 初始化文件,创建flask应用
from flask import Flask
from .config import SQLALCHEMY_DATABASE_URI
from .views import quota_blue
from .exts import init_exts


def create_app():
    app = Flask(__name__)
    #注册蓝图
    app.register_blueprint(blueprint=quota_blue)
    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    # 初始化插件
    init_exts(app)

    return app
