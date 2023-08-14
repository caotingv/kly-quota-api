# 模型 数据库
from .exts import db

# 
class Cpu(db.Model):
    #表名
    __tablename__ = "cpu_motherboard"
    #字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpu_model = db.Column(db.String(32), unique=True, nullable=False)
    cores = db.Column(db.Integer, nullable=False)
    threads = db.Column(db.Integer, nullable=False)
    frequency =  db.Column(db.String(16), nullable=False)
    max_mem_slot = db.Column(db.Integer, nullable=False)
    max_hard_slot = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Mem(db.Model):
    #表名
    __tablename__ = "mem"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mem_model = db.Column(db.String(32), unique=True, nullable=False)
    mem_frequency = db.Column(db.String(16), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    mem_type = db.Column(db.String(8), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Hard(db.Model):
    #表名
    __tablename__ = "hard"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hard_model = db.Column(db.String(32), unique=True, nullable=False)
    interface_type  = db.Column(db.String(16), nullable=False)
    ishdd = db.Column(db.Boolean, default=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)