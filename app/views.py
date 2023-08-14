from flask import Blueprint, request

from app.controllers.cpu import CPUController


from .models import *

quota_blue = Blueprint('quota', __name__)

@quota_blue.route('/')
@quota_blue.route('/version')
def index():
    return {
        'version': 'v1.0.0'
    }

@quota_blue.route('/cpu', methods=['POST'])
def add_cpu():
    cpu_data = request.get_json()
    data = CPUController().add_cpu_info(cpu_data)
    return data
