from flask import Blueprint
from kly_quota_api.db import api
from kly_quota_api.db.models import *

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
    with api.get_session() as session:
        result = session.query(Memory).filter(Memory.id == 1).all()
        for obj in result:
            print(obj.capacity_gb)

    return {
        'message': 'Hello, world!'
    }
