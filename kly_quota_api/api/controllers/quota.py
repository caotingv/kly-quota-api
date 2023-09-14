import math

from flask import jsonify
from kly_quota_api.db.api import DatabaseSessionFactory
from kly_quota_api.db import vendor_repo
from kly_quota_api.db import disk_repo
from kly_quota_api.db import mem_repo
from kly_quota_api.db.models import Vendor


# CPU 超分比
CPU_ALLOCATION_RATIO = 3
# 低、中、高并发
LOW_LEVEL = 0
MID_LEVEL = 1
HIGH_LEVEL = 2

class BaseQuotaContrller(object):
    def __init__(self, request_data) -> None:
        self.db = DatabaseSessionFactory().get_session()
        self.vendor_repo = vendor_repo.VendorRepository()
        self.mem_repo = mem_repo.MemoryRepository()
        self.disk_repo = disk_repo.DiskRepository()
        
        self.edu_info = request_data.get('edu')
        self.bus_info = request_data.get('bus')


    # 教育场景和办公场景都存在时,场景类型以权重最高的为准L
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

        edu_vcpus = math.ceil(edu_flavor.get('vcpu', 0) * edu_vm_num / 3 ) 
        bus_vcpus = math.ceil(bus_flavor.get('vcpu', 0) * bus_vm_num / 3 )
        
        return  edu_vcpus + bus_vcpus

    def calc_vm_nums(self):
        edu_vm_num, bus_vm_num = self.get_vm_nums_from_request()
        
        return  edu_vm_num + bus_vm_num

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

        # Determine the scene weight and weight level
        scene_weight, weight_level = self.calc_concurrency_level()

        # Define filters for server query
        filters = {
            'scene_weight': scene_weight,
            'cpu_vendor': 'Intel'
        }

        with self.db as session:
            intel_server_info = self.vendor_repo.get_all(session, **filters)

        # Calculate the reality concurrency level
        reality_concurrency_level = self.calc_reality_concurrency_level(intel_server_info, weight_level)

        server_info_list = self.query_cpu_threads_data(intel_server_info, reality_concurrency_level)

        return server_info_list

    def calc_reality_concurrency_level(self, intel_server_info, current_level):
        """
        计算出真实需要的服务器的并发等级,例如 2 等级, 一台服务器 cpu 足够使用的情况下, 
        实际也是并发等级为2, 如果不够的情况下, 等级 +1 继续判断。
        :param sql: 一个sql查询对象。
        :vcpu_num: 虚机一共需要的vcpu个数。
        :vm_concurrency_level: 通过虚机个数和场景统计出的并发等级。
        :return: 返回一个int类型的整数, 并发等级, 0 是低并发,1 是中并发,2 是高并发。
        """
        if current_level >= 2:
            return current_level
        
        with self.db as session:
            weight_data = self.vendor_repo.get(session, 
                                               Vendor.concurrency_level == current_level)
        if weight_data is None or self.vcpus >= weight_data.cpu_threads:
            current_level += 1
            return self.calc_reality_concurrency_level(intel_server_info, current_level)
        else:
            return current_level

    def query_cpu_threads_data(self, intel_server_info, concurrency_level):
        """
        根据并发等级查询出低于等于这个等级的所有服务器，并计算出需要的台数
        :param sql: 一个sql查询对象。
        :vcpu_num: 虚机一共需要的vcpu个数。
        :concurrency_level: 统计出的实际的服务器的并发等级。
        :return: 返回一个列表，列表结构为：
            [{
                "number": 2,
                "info": <sql_query_object>
            }]
        """
        with_cpu_threads_list = []

        all_query_data = intel_server_info.filter(Vendor.concurrency_level <= concurrency_level)
        if all_query_data == []:
            raise
        
        for data in all_query_data:
            server_num = self._count_server_num(data.cpu_threads)
     
            with_cpu_threads_list.append(self._build_server_info_dict(server_num, data.cpu_model))
        
        return with_cpu_threads_list

    def _count_server_num(self,server_threads, server_num=1):
        if server_threads * server_num > self.vcpus:
            return server_num
        return self._count_server_num(server_threads, server_num+1)

    def _build_server_info_dict(self, server_num, data):
        return {
            "number": server_num,
            "info": data
        }


class MemoryController(BaseQuotaContrller):
    def __init__(self, request_data):
        super().__init__(request_data)

    def calc_memory_data(self):
        pass


class DiskController(BaseQuotaContrller):
    def __init__(self, request_data):
        super().__init__(request_data)
    
    def calc_disk_data(self):
        pass


class QuotaContrller(BaseQuotaContrller):
    def __init__(self, request_data):
        super().__init__(request_data)
        self.cpu_info = VendorContrller(request_data)
    
    def main(self):
        vendor_info = self.cpu_info.calc_vendor_info()
        
        return {
            'vendor': vendor_info,
            'memory': {},
            'disk': {}
        }


