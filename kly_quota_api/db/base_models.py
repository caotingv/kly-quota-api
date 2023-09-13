from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect

# 创建模型基类
Base = declarative_base()

class QuotaBase:
    def to_dict(self):
        """
        Convert the SQLAlchemy model object to a dictionary.
        """
        return {column.key: getattr(self, column.key) for column in self.__table__.columns}
