from oslo_log import log as logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from kly_quota_api.app import cfg

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


def get_session():
    engine = create_engine(CONF.database.connection)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session
