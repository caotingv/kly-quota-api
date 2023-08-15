from flask import jsonify
from app.exts import db
from app.models import Mem


class MEMController:
    def __init__(self):
        pass

    def add(self, mem_data):
        try:
            new_mem = Mem(**mem_data)
            with db.session.begin():
                db.session.add(new_mem)
            return jsonify({'message': 'mem data added successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
