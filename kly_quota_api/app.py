from flask import Flask
from kly_quota_api.config import Config
from kly_quota_api.api.views import quota_blue
from kly_quota_api.exts import db, migrate


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint=quota_blue)

    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)
    migrate.init_app(db=db, app=app)

    return app

app = create_app()


def main():
    app.run(host='0.0.0.0', debug=True)
