import sys
from os.path import abspath, dirname

from alembic import context
from sqlalchemy import create_engine, pool
from kly_quota_api.db import base_models

sys.path.append(dirname(dirname(abspath(__file__))))

# 获取数据库连接 URL
def get_database_url(config):
    try:
        kly_quota_api_config = config.kly_quota_api_config
        return kly_quota_api_config.database.connection
    except AttributeError:
        print("Error: Please use the kly-db-manage command alembic actions.")
        sys.exit(1)

# 运行迁移脚本
def run_migrations(config, target_metadata):
    url = get_database_url(config)
    
    # 根据是否在线模式选择连接池类
    if context.is_offline_mode():
        engine = create_engine(url)
    else:
        engine = create_engine(url, poolclass=pool.NullPool)

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# 获取数据库模型的元数据
target_metadata = base_models.Base.metadata

# 根据在线/离线模式选择运行迁移
if context.is_offline_mode():
    run_migrations(context.config, target_metadata)
else:
    run_migrations(context.config, target_metadata)
