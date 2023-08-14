from flask import jsonify
from app.exts import db
from app.models import Cpu


class CPUController:
    def __init__(self):
        pass

    def add_cpu_info(self, cpu_data):
        try:
            new_cpu = Cpu(**cpu_data)
            with db.session.begin():
                db.session.add(new_cpu)
            return jsonify({'message': 'CPU data added successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
