# 模型 数据库
from .exts import db


class Cpu(db.Model):
    #表名
    __tablename__ = "cpu_motherboard"
    #字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpu_model = db.Column(db.String(32), unique=True, nullable=False, comment="cpu型号")
    architecture = db.Column(db.String(32), nullable=False, comment="cpu架构,x86_64,aarch64")
    threads = db.Column(db.Integer, nullable=False, comment="cpu线程数")
    frequency =  db.Column(db.String(16), nullable=False, comment="cpu主频")
    max_mem_slot = db.Column(db.Integer, nullable=False, comment="最大内存插槽数")
    max_hard_slot = db.Column(db.Integer, nullable=False, comment="最大硬盘插槽数")
    price = db.Column(db.Float, nullable=False, comment="价格")


class Mem(db.Model):
    #表名
    __tablename__ = "mem"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mem_model = db.Column(db.String(32), unique=True, nullable=False, comment="价格")
    mem_frequency = db.Column(db.String(16), nullable=False, comment="内存主频")
    capacity = db.Column(db.Integer, nullable=False, comment="内存容量")
    mem_type = db.Column(db.String(8), nullable=False, comment="内存类型, ddr3/ddr4")
    price = db.Column(db.Float, nullable=False, comment="价格")

class Disk(db.Model):
    #表名
    __tablename__ = "disk"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hard_model = db.Column(db.String(32), unique=True, nullable=False, comment="硬盘型号")
    interface_type  = db.Column(db.String(16), nullable=False, comment="接口类型")
    ishdd = db.Column(db.Boolean, default=True, nullable=False, comment="是否是机械")
    capacity = db.Column(db.Integer, nullable=False, comment="硬盘容量")
    price = db.Column(db.Float, nullable=False, comment="价格")
