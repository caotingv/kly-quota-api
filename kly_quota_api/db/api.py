from oslo_db import options
from oslo_config import cfg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 初始化配置
CONF = cfg.CONF
options.set_defaults(CONF)
# cfg_file_path = '/etc/kly-quota-api/kly-quota-api.conf'  # 配置文件的路径
# CONF(default_config_files=[cfg_file_path])

# 配置数据库连接
database_url = CONF.database.connection

# 创建数据库会话
def create_database_session():
    # 创建数据库会话
    engine = create_engine(database_url)
    session = sessionmaker(bind=engine)
    return session



# 现在你可以使用session对象执行数据库操作
