from flask import Blueprint,request
from kly_quota_api.db import api
from kly_quota_api.db.models import *
from kly_quota_api.api.controllers.quota import CPUQuery

quota_blue = Blueprint('quota', __name__)
PATH_PREFIX = '/v1.0'

@quota_blue.route('/')
@quota_blue.route('/version')
def index():
    return {
        'version': 'v1.0.0'
    }

@quota_blue.route('/quota', methods=['GET'])
def get_quota():
    data = request.get_json()
    return CPUQuery(data).query_server()
