from flask import Blueprint, request,jsonify

from app.controllers.cpu import CPUController
from app.controllers.mem import MEMController
from app.controllers.disk import DiskController
from app.controllers.quota import query_server
from .models import *

quota_blue = Blueprint('quota', __name__)

@quota_blue.route('/')
@quota_blue.route('/version')
def index():
    return {
        'version': 'v1.0.0'
    }

@quota_blue.route('/<string:device>/add/', methods=['POST'])
def add(device):
    data = request.get_json()
    if device == "cpu":
        reponse_data = CPUController().add(data)
    elif device == "mem":
        reponse_data = MEMController().add(data)
    elif device == "disk":
        reponse_data = DiskController().add(data)
    else:
        return jsonify({'error': "/{}/add/,  Not a correct URL".format(device) }), 404
    return reponse_data
