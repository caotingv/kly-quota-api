import math

from flask import jsonify
from kly_quota_api.db.api import DatabaseSessionFactory
from kly_quota_api.db import vendor_repo
from kly_quota_api.db import disk_repo
from kly_quota_api.db import mem_repo
from kly_quota_api.db.models import Vendor, Memory


# CPU 超分比
CPU_ALLOCATION_RATIO = 3

# 低、中、高并发
LOW_LEVEL = 0
MID_LEVEL = 1
HIGH_LEVEL = 2

SYSTEM_RESERVED_MEM = 48
OSD_RESERVED_MEM = 4
CEPH_RESERVED_MEM = 6


class BaseQuotaContrller(object):
    def __init__(self, request_data) -> None:
        self.db = DatabaseSessionFactory().get_session()
        self.vendor_repo = vendor_repo.VendorRepository()
        self.mem_repo = mem_repo.MemoryRepository()
        self.disk_repo = disk_repo.DiskRepository()

        self.edu_info = request_data.get('edu', {})
        self.bus_info = request_data.get('bus', {})

    # 教育场景和办公场景都存在时,场景类型以权重最高的为准

    def calc_concurrency_level(self):
        edu_weight = self.edu_info.get('weight', 0)
        bus_weight = self.bus_info.get('weight', 0)

        weight = max(edu_weight, bus_weight)
        edu_vm_num, bus_vm_num = self.get_vm_nums_from_request()
        vm_num = edu_vm_num + bus_vm_num

        if weight == 0:
            if vm_num <= 30:
                return weight, LOW_LEVEL
            elif vm_num <= 48:
                return weight, MID_LEVEL
        else:
            if vm_num <= 31:
                return weight, LOW_LEVEL

        return weight, HIGH_LEVEL

    def calc_vcpu_nums(self):
        edu_vm_num, bus_vm_num = self.get_vm_nums_from_request()
        edu_flavor, bus_flavor = self.get_flavor_from_request()

        edu_vcpus = math.ceil(edu_flavor.get('vcpu', 0) * edu_vm_num / 3)
        bus_vcpus = math.ceil(bus_flavor.get('vcpu', 0) * bus_vm_num / 3)

        return edu_vcpus + bus_vcpus

    def calc_mem_nums(self):
        edu_vm_num, bus_vm_num = self.get_vm_nums_from_request()
        edu_flavor, bus_flavor = self.get_flavor_from_request()
        edu_mems = edu_flavor.get('memory', 0) * \
            edu_vm_num - SYSTEM_RESERVED_MEM
        bus_mems = bus_flavor.get('memory', 0) * bus_vm_num - CEPH_RESERVED_MEM

        return edu_mems + bus_mems

    def calc_vm_nums(self):
        edu_vm_num, bus_vm_num = self.get_vm_nums_from_request()

        return edu_vm_num + bus_vm_num

    def get_vm_nums_from_request(self):
        edu_vm_num = self.edu_info.get('number', 0)
        bus_vm_num = self.bus_info.get('number', 0)

        return edu_vm_num, bus_vm_num

    def get_flavor_from_request(self):
        edu_flavor = self.edu_info.get('flavor', {})
        bus_flavor = self.bus_info.get('flavor', {})

        return edu_flavor, bus_flavor


class VendorContrller(BaseQuotaContrller):
    def __init__(self, request_data):
        super().__init__(request_data)
        self.vcpus = self.calc_vcpu_nums()

    def calc_vendor_info(self):
        if not self.edu_info and not self.bus_info:
            return jsonify({'error': "Scenario type not defined"})

        # 计算并获取场景权重和权重级别
        scene_weight, weight_level = self.calc_concurrency_level()

        # 定义用于服务器查询的过滤器
        filters = {
            'scene_weight': scene_weight,
            'cpu_vendor': 'Intel'
        }

        with self.db as session:
            vendor_intel_info = self.vendor_repo.get_all(session, **filters)

        # 计算所需的实际并发等级
        required_concurrency_level = self.calc_required_concurrency_level(
            vendor_intel_info, weight_level)

        # 查询符合所需并发等级的服务器信息
        server_info_list = self.query_servers_by_concurrency(
            vendor_intel_info, required_concurrency_level)

        return server_info_list

    def calc_required_concurrency_level(self, intel_server_info, current_level):
        """
        计算所需的服务器并发等级。如果当前等级足够，返回当前等级；否则，递归计算所需等级。

        :param intel_server_info: 包含服务器信息的数据对象或查询结果。
        :param current_level: 当前的并发等级。

        :return: 所需的服务器并发等级（0 表示低并发，1 表示中并发，2 表示高并发）。
        """
        if current_level >= 2:
            return current_level

        with self.db as session:
            level_data = self.vendor_repo.get(
                session, Vendor.concurrency_level == current_level)

        if level_data is None or self.vcpus >= level_data.cpu_threads:
            return current_level
        else:
            return self.calc_required_concurrency_level(intel_server_info, current_level + 1)

    def query_servers_by_concurrency(self, intel_server_info, target_concurrency):
        """
        查询符合目标并发等级的服务器信息，并计算所需服务器数量。

        :param intel_server_info: 包含服务器信息的数据对象或查询结果。
        :param target_concurrency: 目标并发等级。

        :return: 包含所需服务器数量和信息的字典列表。
        """
        servers_with_threads = []

        # 筛选符合目标并发等级要求的服务器
        filtered_servers = [
            server for server in intel_server_info if server.concurrency_level <= target_concurrency]

        # 如果没有符合条件的服务器，可以根据需求抛出异常或采取其他操作
        if not filtered_servers:
            raise Exception(
                "No servers found for the target concurrency level")

        # 遍历筛选后的服务器列表，计算所需服务器数量并构建信息字典
        for server in filtered_servers:
            required_server_count = self._count_server_num(server.cpu_threads)
            server_info = self._build_server_info_dict(
                required_server_count, server)
            servers_with_threads.append(server_info)

        return servers_with_threads

    def _count_server_num(self, server_threads, server_num=1):
        if server_threads * server_num > self.vcpus:
            return server_num

        return self._count_server_num(server_threads, server_num + 1)

    def _build_server_info_dict(self, server_num, data):
        return {
            "number": server_num,
            "vendor": {
                "vendor": data.vendor,
                "cpu_model": data.cpu_model,
                "max_mem": data.max_mem,
                # "max_sata_hard": data.max_sata_hard,
                # "max_nvme_hard": data.max_nvme_hard,
            }
        }


class DiskController(BaseQuotaContrller):
    def __init__(self, request_data):
        super().__init__(request_data)
        self.sata_capacity, self.nvme_capacity = self.get_disk_capacity()

    def calc_disk_info(self):
        edu_vm_num, bus_vm_num = self.get_vm_nums_from_request()
        edu_flavor, bus_flavor = self.get_flavor_from_request()

        disk_info = {}

        if bus_vm_num:
            disk_info['bus'] = self.calc_bus_disk_device(
                bus_vm_num, bus_flavor)

        if edu_vm_num:
            disk_info['edu'] = self.calc_edu_disk_device(
                edu_vm_num, edu_flavor)

        return disk_info

    def calc_bus_disk_device(self, vm_num, flavor):
        sata_disk_num = math.ceil(vm_num / 8)
        nvme_disk_num = math.ceil(sata_disk_num / 6)

        sata_required_storage = vm_num * flavor.get('storage') * 2 / 0.8
        nvme_required_storage = sata_required_storage / 20

        sata_disk_num, sata_capacity_gb = self.find_closest_greater_capacity(
            sata_required_storage, sata_disk_num, self.sata_capacity)
        nvme_disk_num, nvme_capacity_gb = self.find_closest_greater_capacity(
            nvme_required_storage, nvme_disk_num, self.nvme_capacity)

        return {
            'sata_num':  sata_disk_num,
            'sata_capacity_gb': sata_capacity_gb,
            'nvme_num':  nvme_disk_num,
            'nvme_capacity_gb': nvme_capacity_gb
        }

    def calc_edu_disk_device(self, vm_num, flavor):
        nvme_disk_num = math.ceil(vm_num / 20)
        nvme_required_storage = vm_num * flavor.get('storage') / 0.8
        nvme_disk_num, nvme_capacity_gb = self.find_closest_greater_capacity(
            nvme_required_storage, nvme_disk_num, self.nvme_capacity)

        return {
            'sata_num':  0,
            'sata_capacity_gb': 0,
            'nvme_num':  nvme_disk_num,
            'nvme_capacity_gb': nvme_capacity_gb
        }

    def find_closest_greater_capacity(self, storage, disk_num, capacity_list):
        capacity_gb = storage / disk_num
        capacity_list.sort()

        for capacity in capacity_list:
            if capacity >= capacity_gb:
                return disk_num, capacity

        disk_num += 1
        return self.find_closest_greater_capacity(storage, disk_num, capacity_list)

    def get_disk_capacity(self):
        sata_capacity = []
        nvme_capacity = []

        with self.db as session:
            devices = self.disk_repo.get_all(session)

        for device in devices:
            disk_dict = device.to_dict()

            if disk_dict.get('interface_type') == 'SATA':
                sata_capacity.append(disk_dict.get('capacity_tb') * 1000)

            if disk_dict.get('interface_type') == 'NVMe':
                nvme_capacity.append(disk_dict.get('capacity_tb') * 1000)

        return sata_capacity, nvme_capacity


class MemoryController(BaseQuotaContrller):
    def __init__(self, request_data):
        super().__init__(request_data)
        self.mems = self.calc_mem_nums()
        self.edu_vm_mum , self.bus_vm_mum = self.get_vm_nums_from_request()
        edu_vm_mems, bus_vm_mems = self.get_vm_mems()
        self.total_vm_mems = bus_vm_mems + edu_vm_mems

    def calc_memory_info(self, disk_num, vendor):
        server_number = vendor.get('number')
        if self.bus_vm_mum != 0:
            self.total_vm_mems += (SYSTEM_RESERVED_MEM + CEPH_RESERVED_MEM) * \
                server_number + OSD_RESERVED_MEM * disk_num
        else:
            self.total_vm_mems += SYSTEM_RESERVED_MEM * server_number
        ave_server_mem = math.ceil(
            self.total_vm_mems / server_number / vendor['vendor'].get('max_mem', 0))
        mem_card_size = self._find_nearby_two_power(ave_server_mem)
        mem_card_number = math.ceil(
            self.total_vm_mems / server_number / mem_card_size)

        db = DatabaseSessionFactory().get_session()
        filters = {
            'capacity_gb': mem_card_size
        }

        with db as session:
            mem_card_data = self.mem_repo.get(session,  **filters)
            vendor['memory'] = self._build_mem_data(
                mem_card_number, mem_card_data)
        return vendor
    
    def get_vm_mems(self):
        edu_vm_mems = 0
        bus_vm_mems = 0
        if self.edu_vm_mum != 0:
            edu_vm_mems =  self.edu_vm_mum * \
            self.edu_info['flavor']['memory']
        if self.bus_vm_mum != 0:
            bus_vm_mems = self.bus_vm_mum * \
            self.bus_info['flavor']['memory']

        return edu_vm_mems,bus_vm_mems

    def _build_mem_data(self, number, mem_card_data):
        return {
            'number': number,
            'mem_info': {
                'vendor': mem_card_data.vendor,
                'mem_frequency': mem_card_data.mem_frequency,
                'mem_version': mem_card_data.mem_version,
                'size': mem_card_data.capacity_gb,
            }
        }

    def _find_nearby_two_power(self, digit):
        if digit <= 32:
            return 32
        else:
            digit |= digit >> 1
            digit |= digit >> 2
            digit |= digit >> 4
            digit |= digit >> 8
            digit |= digit >> 16
            return digit + 1


class QuotaContrller(BaseQuotaContrller):
    def __init__(self, request_data):
        super().__init__(request_data)
        self.vendor_info = VendorContrller(request_data)
        self.disk_info = DiskController(request_data)
        self.memory_info = MemoryController(request_data)

    def _calculate_disk_info(self, vendor_num, disk_dvice):
        num_nvme = disk_dvice.get('nvme_num', 0)
        num_sata = disk_dvice.get('sata_num', 0)
        nvme_size = disk_dvice.get('nvme_capacity_gb', 0)
        sata_size = disk_dvice.get('sata_capacity_gb', 0)

        return {
            'nvme_num': math.ceil(num_nvme / vendor_num),
            'nvme_size': nvme_size,
            'sata_num': math.ceil(num_sata / vendor_num),
            'sata_size': sata_size,
        }

    def main(self):
        server_info_list = []

        vendor_info_data = self.vendor_info.calc_vendor_info()
        disk_info_data = self.disk_info.calc_disk_info()
        disk_num = disk_info_data.get('bus', {}).get('sata_num', 0)

        for vendor in vendor_info_data:
            vendor_num = vendor.get('number', 0)
            bus_disk_dvice = disk_info_data.get('bus', {})
            edu_disk_dvice = disk_info_data.get('edu', {})

            bus_disk_info = self._calculate_disk_info(
                vendor_num, bus_disk_dvice)
            edu_disk_info = self._calculate_disk_info(
                vendor_num, edu_disk_dvice)

            server_info = self.memory_info.calc_memory_info(disk_num, vendor)
            server_info['disk'] = {
                'bus_disk': bus_disk_info,
                'edu_disk': edu_disk_info,
            }

            server_info_list.append(server_info)

        return server_info_list
