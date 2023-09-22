from sqlalchemy import Column, Integer, String, Float, Boolean
from kly_quota_api.db import base_models


# 定义 Vendor 模型
class Vendor(base_models.Base, base_models.QuotaBase):
    __tablename__ = "vendor"
    id = Column(Integer, primary_key=True, autoincrement=True)
    vendor = Column(String(64), nullable=False, comment="主板制造商:安擎,国鑫")
    cpu_vendor = Column(String(64), nullable=False, comment="intel, amd")
    cpu_model = Column(String(32), nullable=False, comment="CPU型号")
    cpu_architecture = Column(String(32), nullable=False, comment="CPU架构, x86_64, aarch64")
    cpu_threads = Column(Integer, nullable=False, comment="CPU线程数")
    cpu_frequency = Column(String(16), nullable=False, comment="CPU主频")
    max_cpu = Column(Integer, nullable=False, comment="最大CPU插槽数")
    max_mem = Column(Integer, nullable=False, comment="最大内存插槽数")
    max_sata_hard = Column(Integer, nullable=False, comment="最大SATA硬盘插槽数")
    max_nvme_hard = Column(Integer, nullable=False, comment="最大NVME硬盘插槽数")
    scene_weight = Column(Integer, nullable=False, comment="场景权重")
    concurrency_level = Column(Integer, nullable=False, comment="并发等级 0 低并发 1 中并发 2 高并发")


# 定义 Memory 模型
class Memory(base_models.Base, base_models.QuotaBase):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    capacity_gb = Column(Integer, nullable=False, comment="内存容量,单位GB")
    vendor = Column(String(64), nullable=True, comment="内存厂商")
    mem_frequency = Column(Integer, nullable=False, comment="内存主频")
    mem_version = Column(String(8), nullable=False, comment="几代内存,DDR4..")


# 定义 Disk 模型
class Disk(base_models.Base, base_models.QuotaBase):
    __tablename__ = "disk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    interface_type = Column(String(16), nullable=False, comment="接口类型")
    is_hdd = Column(Boolean, nullable=False, comment="是否是机械硬盘")
    capacity_tb = Column(Float, nullable=False, comment="硬盘容量,单位TB")
    physical_size = Column(String(16), nullable=True, comment="物理尺寸")
    transfer_speed = Column(String(16), nullable=True, comment="传输速度")
    rotation_speed = Column(String(16), nullable=True, comment="旋转速度")
