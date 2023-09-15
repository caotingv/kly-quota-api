from kly_quota_api.db import base_repo
from kly_quota_api.db import models


class DiskRepository(base_repo.BaseRepository):

    model_class = models.Disk
