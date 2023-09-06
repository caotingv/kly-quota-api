from flask import Flask
from kly_quota_api.api.views import quota_blue


app = Flask(__name__)
app.register_blueprint(blueprint=quota_blue)


def main():
    app.run(host='0.0.0.0', debug=True)
