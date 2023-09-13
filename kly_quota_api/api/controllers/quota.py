import math

from flask import jsonify
from kly_quota_api.db import api
from kly_quota_api.db import vendor_repo
from kly_quota_api.db import disk_repo
from kly_quota_api.db import mem_repo
from kly_quota_api.db.models import Vendor


CPU_ALLOCATION_RATIO = 3
LOW_LEVEL = 0
MID_LEVEL = 1
HIGH_LEVEL = 2

class Query(object):
    def __init__(self,filter_dict) -> None:
        self.edu_info = filter_dict.get('edu')
        self.bus_info = filter_dict.get('bus')
        self.vm_num = 0
        self.vcpus = 0
        self.session = api.get_session()
        self.vendor_repo = vendor_repo.VendorRepository()
        self.mem_repo = mem_repo.MemoryRepository()
        self.disk_repo = disk_repo.DiskRepository()


    def query_scene_weight(self):
        # 教育场景和办公场景都存在时,场景类型以权重最高的为准
        weight = ""
        if self.edu_info and self.bus_info:
            if self.edu_info.get('weight') >= self.bus_info.get('weight'):
                self.weight = self.edu_info.get('weight')
            else:
                self.weight = self.bus_info.get('weight')
        elif self.edu_info:
            weight = self.edu_info.get('weight')
        elif self.bus_info:
            weight = self.bus_info.get('weight')
        return weight
    
    def query_vcpus_vms_num(self):
        # 查询虚拟机数量及vcpu数量 vm_num vcpus_num
        if self.edu_info and self.bus_info:
            self.vm_num = self.edu_info['number'] + self.bus_info['number']
            self.vcpus = math.ceil((self.edu_info['flavor']['vcpu'] * self.edu_info['number'] + \
                self.bus_info['flavor']['vcpu'] * self.bus_info['number'])/3)
        elif self.edu_info:
            self.vm_num = self.edu_info['number']
            self.vcpus = math.ceil(self.edu_info['flavor']['vcpu'] * self.edu_info['number']/3)
        elif self.bus_info:
            self.vm_num = self.bus_info['number']
            self.vcpus = math.ceil(self.bus_info['flavor']['vcpu'] * self.edu_info['number']/3)
    
    def from_weight_get_level(self, scene_weight):
        # 查询虚拟机并发等级
        if scene_weight == 0:
            if self.vm_num <= 30:
                concurrency_level = LOW_LEVEL
            elif 31 <= self.vm_num <= 48:
                concurrency_level = MID_LEVEL
            else:
                concurrency_level = HIGH_LEVEL
        else:
            if self.vm_num <= 31:
                concurrency_level = LOW_LEVEL
            else:
                concurrency_level = HIGH_LEVEL
        return concurrency_level

class CPUQuery(Query):

    def query_reality_concurrency_level(self, intel_server_info, weight_level):
        """
        计算出真实需要的服务器的并发等级,例如2等级, 一台服务器cpu足够使用的情况下, 实际也是并发等级为2,如果不够的情况下, 等级+1继续判断。
        :param sql: 一个sql查询对象.
        :vcpu_num: 虚机一共需要的vcpu个数.
        :vm_concurrency_level: 通过虚机个数和场景统计出的并发等级.
        :return: 返回一个int类型的整数,并发等级, 0低并发,1中并发,2高并发
        """
        
        # 计算实际并发等级
        if weight_level >= 2:
            return weight_level
        weight_data = self.vendor_repo.get(self.session, Vendor.concurrency_level == weight_level)
        if weight_data is None or self.vcpus >= weight_data.cpu_threads:
            weight_level += 1
            return self.query_reality_concurrency_level(intel_server_info, weight_level)
        else:
            return weight_level

    def query_cpu_threads_data(self, intel_server_info, concurrency_level):
        """
        根据并发等级查询出低于等于这个等级的所有服务器，并计算出需要的台数
        :param sql: 一个sql查询对象.
        :vcpu_num: 虚机一共需要的vcpu个数.
        :concurrency_level: 统计出的实际的服务器的并发等级.
        :return: 返回一个列表，列表结构为[{
        "number": 2,
        "info": <sql_query_object>
        }...]
        """
        with_cpu_threads_list = []
        filters = {'cpu_vendor': 'Intel',
                   'concurrency_level': concurrency_level}
        all_query_data = intel_server_info.filter(Vendor.concurrency_level <= concurrency_level)
        if all_query_data == []:
            raise
        for data in all_query_data:
            server_num = self._count_server_num(data.cpu_threads, self.vcpus)
            print(" server_num is ", server_num)
            print(" cpu_threads is ", data.cpu_threads)
            print(" vcpus is ", self.vcpus)
            print(" cpu_model is ", data.cpu_model)
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

    def query_server(self):
        if not self.edu_info and not self.bus_info:
            return jsonify({'error': "Scenario type not defined"})
        # 查询场景权重 0 轻载 1 重载
        scene_weight = self.query_scene_weight()
        self.query_vcpus_vms_num()
        weight_level = self.from_weight_get_level(scene_weight)

        # 查询满足条件的服务器
        filters = {
            'scene_weight': scene_weight,
            'cpu_vendor': 'Intel'
        }
        intel_server_info = self.vendor_repo.get_all(self.session, **filters)
        reality_concurrency_level = self.query_reality_concurrency_level(intel_server_info, weight_level)
        server_info_list = self.query_cpu_threads_data(intel_server_info, reality_concurrency_level)
        return server_info_list


class DiskQuery(Query):
    def __init__(self, request_data):
        self.db = DatabaseSessionFactory().get_session()
        self.disk_repo = DiskRepository()
        self.request_data = request_data
    
    def compute_disk_data(self):
        pass

    def query_disk_data(self, interface_type):
        with self.db as session:
            results = self.disk_repo.get_by_interface_type(
                                        session=session, 
                                        interface_type=interface_type)
       
        return results
