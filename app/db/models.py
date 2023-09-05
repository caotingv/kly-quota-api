from api.exts import db


class Motherboard(db.Model):

    __tablename__ = "motherboard"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manufacturer = db.Column(db.String(64), nullable=False, comment="主板制造商:安擎,国鑫")
    cpu_model = db.Column(db.String(32), nullable=False, comment="CPU型号")
    cpu_architecture = db.Column(
        db.String(32), nullable=False, comment="CPU架构, x86_64, aarch64")
    cpu_threads = db.Column(db.Integer, nullable=False, comment="CPU线程数")
    cpu_frequency = db.Column(db.String(16), nullable=False, comment="CPU主频")
    max_cpu = db.Column(db.Integer, nullable=False, comment="最大CPU插槽数")
    max_mem = db.Column(db.Integer, nullable=False, comment="最大内存插槽数")
    max_sata_hard = db.Column(db.Integer, nullable=False, comment="最大SATA硬盘插槽数")
    max_nvme_hard = db.Column(db.Integer, nullable=False, comment="最大NVME硬盘插槽数")

class Memory(db.Model):

    __tablename__ = "memory"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    capacity_gb = db.Column(db.Integer, nullable=False, comment="内存容量,单位GB")

class Disk(db.Model):

    __tablename__ = "disk"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interface_type = db.Column(db.String(16), nullable=False, comment="接口类型")
    is_hdd = db.Column(db.Integer, nullable=False, comment="是否是机械硬盘")
    capacity_gb = db.Column(db.Integer, nullable=False, comment="硬盘容量,单位GB")
