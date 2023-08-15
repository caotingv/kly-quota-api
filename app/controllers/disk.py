from flask import jsonify
from app.exts import db
from app.models import Disk


class DiskController:
    def __init__(self):
        pass

    def add(self, disk_data):
        try:
            new_disk = Disk(**disk_data)
            with db.session.begin():
                db.session.add(new_disk)
            return jsonify({'message': 'disk data added successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
