from ..exts import db


class Disk(db.Model):

    __tablename__ = "disk"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interface_type = db.Column(db.String(16), nullable=False, comment="接口类型")
    is_hdd = db.Column(db.Integer, nullable=False, comment="是否是机械硬盘")
    capacity_gb = db.Column(db.Integer, nullable=False, comment="硬盘容量,单位GB")
