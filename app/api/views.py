from db.models import *
from flask import Blueprint

quota_blue = Blueprint('quota', __name__)


@quota_blue.route('/')
@quota_blue.route('/version')
def index():
    return {
        'version': 'v1.0.0'
    }
