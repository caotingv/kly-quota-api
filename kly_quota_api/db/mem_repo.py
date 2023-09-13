from kly_quota_api.db import base_repo
from kly_quota_api.db import models


class MemoryRepository(base_repo.BaseRepository):
    model_class = models.Memory
