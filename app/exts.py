#exts.py 插件管理 扩展的第三方插件
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#初始化
db = SQLAlchemy() # ORM
migrate = Migrate() # 数据迁移

def init_exts(app):
    db.init_app(app)
    migrate.init_app(db=db,app=app)