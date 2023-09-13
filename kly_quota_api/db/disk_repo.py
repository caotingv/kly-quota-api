from kly_quota_api.db import base_repo
from kly_quota_api.db import models


class DiskRepository(base_repo.BaseRepository):

    model_class = models.Disk

    def get_by_interface_type(self, session, interface_type, **filters):
        result_dicts = []

        query = session.query(self.model_class)
        devices = query.filter().filter_by(interface_type=interface_type, **filters).all()
        
        for device in devices:
            disk_dict = device.to_dict()  # 将每个Disk对象转换为字典
            result_dicts.append(disk_dict)

        return result_dicts
