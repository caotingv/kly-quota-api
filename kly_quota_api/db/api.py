from contextlib import contextmanager
from oslo_log import log as logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from oslo_config import cfg

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class DatabaseSessionFactory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSessionFactory, cls).__new__(cls)
            cls._instance._engine = create_engine(CONF.database.connection)
            cls._instance._Session = sessionmaker(bind=cls._instance._engine)
        return cls._instance

    @contextmanager
    def get_session(self):
        session = self._Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
