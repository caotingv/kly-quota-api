from ..exts import db


class Memory(db.Model):

    __tablename__ = "memory"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    capacity_gb = db.Column(db.Integer, nullable=False, comment="内存容量,单位GB")
