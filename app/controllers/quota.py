from flask import jsonify
from app.exts import db
from app.models import Cpu
import json
def query_server(condition):
    filter_dict = json.dumps(condition)
    edu_info = filter_dict.get('edu')
    bus_info = filter_dict.get('bus')
    if not edu_info and not bus_info:
        return jsonify({'error':"Scenario type not defined"})
    
    # 教育场景和办公场景都存在时,场景类型以权重最高的为准
    scene=""
    if edu_info and bus_info:
        if edu_info.get('weight') >= bus_info.get('weight'):
            scene = edu_info.get('scene')
        else:
            scene = bus_info.get('scene')
    elif edu_info:
        scene = edu_info.get('scene')
    elif bus_info:
        scene = bus_info.get('scene')
    
    
