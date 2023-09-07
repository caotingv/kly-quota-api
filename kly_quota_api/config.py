class Config:
    # Flask应用程序的通用配置
    DEBUG = True  # 启用调试模式

    # 数据库配置
    SQL_IPADDR = '172.18.107.106'
    SQL_PASS = '123456'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{SQL_PASS}@{SQL_IPADDR}:3306/klc_quota?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭对模型更改的跟踪
    SQLALCHEMY_ECHO = True  # 在控制台上显示生成的SQL语句（在开发中很有用）
