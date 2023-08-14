# __inint__.py 初始化文件,创建flask应用
from flask import Flask
from .views import blue
from .exts import init_exts


def create_app():
    app = Flask(__name__)
    #注册蓝图
    app.register_blueprint(blueprint=blue)
    # 配置数据库
    SQLHOSTNAME = "172.18.107.106"
    PORT = 3306
    USERNAME = "root"
    PASSWORD = "123456"
    DATABASE = "database_test"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{SQLHOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    # 初始化插件
    init_exts(app)

    return app