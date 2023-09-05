# __inint__.py 初始化文件,创建flask应用
from flask import Flask
from .config import SQLALCHEMY_DATABASE_URI
from .views import quota_blue
from .exts import init_exts


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint=quota_blue)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    init_exts(app)

    return app
