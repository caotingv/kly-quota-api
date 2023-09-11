import sys
from flask import Flask
from kly_quota_api.common import service
from kly_quota_api.api.views import quota_blue
from oslo_config import cfg
from oslo_db import options
from oslo_log import log as logging


LOG = logging.getLogger(__name__)
CONF = cfg.CONF
PATH_PREFIX = '/v1.0'

def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint=quota_blue, url_prefix=PATH_PREFIX)
    return app

def run_app(app, host='0.0.0.0', port=8080):
    service.prepare_service(sys.argv)
    cfg.CONF.log_opt_values(LOG, logging.INFO)

    app.run(host=host, port=port, debug=cfg.CONF.DEFAULT.debug)

def main():
    app = create_app()

    run_app(app, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
