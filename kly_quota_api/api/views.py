from flask import Blueprint

quota_blue = Blueprint('quota', __name__)
PATH_PREFIX = '/v1.0'

@quota_blue.route('/')
@quota_blue.route('/version')
def index():
    return {
        'version': 'v1.0.0'
    }

@quota_blue.route('/quota')
def get_quota():
    """
    Get quota information.
    """
    return {
        'message': 'Hello, world!'
    }
