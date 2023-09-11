import sys
from oslo_config import cfg
from oslo_log import log as logging
from kly_quota_api import version

LOG = logging.getLogger(__name__)

default_ops = [
    cfg.BoolOpt('debug', default=False, help='Enable debug mode')
]

database_opts = [
    cfg.BoolOpt('sqlalchemy_track_modifications',
                default=False, help='Track modifications to SQLAlchemy models'),
    cfg.BoolOpt('sqlalchemy_echo', default=False,
                help='Display generated SQL statements'),
    cfg.StrOpt('connection', default='',
               help='Database connection string')
]

core_cli_opts = []
cfg.CONF.register_opts(default_ops, group='DEFAULT')
cfg.CONF.register_opts(database_opts, group='database')


def register_cli_opts():
    cfg.CONF.register_cli_opts(core_cli_opts)
    logging.register_options(cfg.CONF)


def init(args, **kwargs):
    register_cli_opts()
    cfg.CONF(args=args, project='kly-quota-api',
             version='%%prog %s' % version.version_info.release_string(),
             **kwargs)


def setup_logging(conf):
    """Sets up the logging options for a log with supplied name.

    :param conf: a cfg.ConfOpts object
    """
    product_name = "kly-quota-api"
    logging.setup(conf, product_name)
    LOG.info("Logging enabled!")
    LOG.info("%(prog)s version %(version)s",
             {'prog': sys.argv[0],
              'version': version.version_info.release_string()})
    LOG.debug("command line: %s", " ".join(sys.argv))

# print("The value of option1 is %s" % cfg.CONF.database.connection)
# print("The value of option2 is %d" % cfg.CONF.database.sqlalchemy_echo)
