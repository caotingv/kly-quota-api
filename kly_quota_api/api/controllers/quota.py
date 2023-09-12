import math

from flask import jsonify

from kly_quota_api.db.models import Motherboard
from kly_quota_api.db import api

CPU_ALLOCATION_RATIO = 3


class Query(object):
    def __init__(self, filter_dict) -> None:
        self.edu_info = filter_dict.get('edu')
        self.bus_info = filter_dict.get('bus')
        self.cli_num = 0
        self.vcpus = 0
        self.db = api.get_session()

    def query_scene_weight(self):
        # 教育场景和办公场景都存在时,场景类型以权重最高的为准
        weight = ""
        if self.edu_info and self.bus_info:
            if self.edu_info.get('weight') >= self.bus_info.get('weight'):
                weight = self.edu_info.get('weight')
            else:
                weight = self.bus_info.get('weight')
        elif self.edu_info:
            weight = self.edu_info.get('weight')
        elif self.bus_info:
            weight = self.bus_info.get('weight')
        return weight

    def query_cli_flavor(self):
        # 统计数量和需要的cpu数量, cpu超配比为3
        if self.edu_info and self.bus_info:
            self.cli_num = self.edu_info['number'] + self.bus_info['number']
            self.vcpus = math.ceil((self.edu_info['flavor']['vcpu'] * self.edu_info['number'] +
                                   self.bus_info['flavor']['vcpu'] * self.bus_info['number'])/3)
        elif self.edu_info:
            self.cli_num = self.edu_info['number']
            self.vcpus = math.ceil(
                self.edu_info['flavor']['vcpu'] * self.edu_info['number']/3)
        elif self.bus_info:
            self.cli_num = self.bus_info['number']
            self.vcpus = math.ceil(
                self.bus_info['flavor']['vcpu'] * self.edu_info['number']/3)

    def query_scene_sql(self, weight, cpu_manufacturer):
        """
        通过场景和cpu型号初步筛选符合条件的服务器信息, 因为场景直接决定cpu, amd和intel的cpu核心数不一致,最后返回的方案中需要amd和intel分开.

        :param weight: 使用场景权重, 0 or 1,0: 轻载、普教, 1: 重载
        :cpu_manufacturer: cpu 厂商, intel or amd
        :return: 返回一个带有场景和cpu厂商filter条件的查询对象, 可以继续使用flask-SQLAlchemy查询方法进行查询.
        """

        try:
            # all_scene_motherboard = db.session.query(Motherboard).filter(Motherboard.weight == weight).filter(Motherboard.manufacturer == server_producer).filter(Motherboard.cpu_producer == cpu_producer).all()
            all_scene_motherboard_sql = self.db.query(Motherboard).filter(
                Motherboard.scene_weight == weight, Motherboard.cpu_model.startswith(cpu_manufacturer))
            return all_scene_motherboard_sql
        except Exception as e:
            raise e


class CPUQuery(Query):
    # 确定虚机需要并发的等级, 0低并发，1中并发,2高并发
    def query_cli_concurrency_level(self, scene_weight):
        """
        通过虚机个数和场景统计出并发等级, 0低并发,1中并发,2高并发

        :param cli_num: 虚机个数.
        :scene_weight: 使用场景权重, 0 or 1,0: 轻载、普教, 1: 重载.
        :return: 返回一个int类型的整数,并发等级, 0低并发,1中并发,2高并发
        """

        if scene_weight == 0:
            if self.cli_num <= 30:
                concurrency_level = 0
            elif 31 <= self.cli_num <= 48:
                concurrency_level = 1
            else:
                concurrency_level = 2
        else:
            if self.cli_num <= 31:
                concurrency_level = 0
            else:
                concurrency_level = 2
        return concurrency_level

    def query_reality_concurrency_level(self, sql, cli_concurrency_level):
        """
        计算出真实需要的服务器的并发等级,例如2等级, 一台服务器cpu足够使用的情况下, 实际也是并发等级为2,如果不够的情况下, 等级+1继续判断。

        :param sql: 一个sql查询对象.
        :vcpu_num: 虚机一共需要的vcpu个数.
        :cli_concurrency_level: 通过虚机个数和场景统计出的并发等级.
        :return: 返回一个int类型的整数,并发等级, 0低并发,1中并发,2高并发
        """

        if cli_concurrency_level >= 2:
            return cli_concurrency_level
        with_concurrency_sql = sql.filter(
            Motherboard.concurrency_level == cli_concurrency_level).first()
        if with_concurrency_sql is None or self.vcpus >= with_concurrency_sql.cpu_threads * with_concurrency_sql.max_cpu:
            cli_concurrency_level += 1
            return self.query_reality_concurrency_level(sql, self.vcpus, cli_concurrency_level)
        else:
            return cli_concurrency_level

    def query_cpu_threads_data(self, sql, concurrency_level):
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
        all_query_data = sql.filter(
            Motherboard.concurrency_level <= concurrency_level).all()
        if all_query_data == []:
            raise
        for data in all_query_data:
            print(data.cpu_model, data.cpu_threads, self.vcpus)
            server_num = self._count_server_num(
                data.cpu_threads * data.max_cpu)
            with_cpu_threads_list.append(
                self._build_server_info_dict(server_num, data.cpu_model))
        return with_cpu_threads_list

    def _count_server_num(self, server_threads, server_num=1):
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
        scene_weight = self.query_scene_weight()
        print(scene_weight)
        self.query_cli_flavor()
        cli_concurrency_level = self.query_cli_concurrency_level(scene_weight)
        intel_server_info = self._server_cpu_query(
            'intel', scene_weight, cli_concurrency_level)
        # amd_server_info = server_cpu_query('AMD',scene_weight,cli_concurrency_level,vcpus)
        return jsonify(intel_server_info)

    def _server_cpu_query(self, cpu_manufacturer, scene_weight, cli_concurrency_level):
        all_sql_query = self.query_scene_sql(scene_weight, cpu_manufacturer)
        reality_concurrency_level = self.query_reality_concurrency_level(
            all_sql_query, cli_concurrency_level)
        server_info_list = self.query_cpu_threads_data(
            all_sql_query, reality_concurrency_level)
        return server_info_list
