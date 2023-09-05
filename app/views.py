from flask import Blueprint
from .models.disk import Disk
from .models.memory import Memory
from .models.motherboard import Motherboard


quota_blue = Blueprint('quota', __name__)


@quota_blue.route('/')
@quota_blue.route('/version')
def index():
    return {
        'version': 'v1.0.0'
    }
