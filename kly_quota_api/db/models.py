from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base


# 创建模型基类
Base = declarative_base()

# 定义 Motherboard 模型
class Motherboard(Base):
    __tablename__ = "motherboard"

    uuid = Column(String(128), primary_key=True)
    manufacturer = Column(String(64), nullable=False, comment="主板制造商:安擎,国鑫")
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
    cpu_producer = Column(String(32), nullable=False, comment="cpu厂商")

# 定义 Memory 模型
class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    capacity_gb = Column(Integer, nullable=False, comment="内存容量,单位GB")

# 定义 Disk 模型
class Disk(Base):
    __tablename__ = "disk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    interface_type = Column(String(16), nullable=False, comment="接口类型")
    is_hdd = Column(Boolean, nullable=False, comment="是否是机械硬盘")
    capacity_tb = Column(Float, nullable=False, comment="硬盘容量,单位TB")
