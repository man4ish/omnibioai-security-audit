import redis
import json
from audit.config import AuditConfig


class StreamReader:
    def __init__(self):
        self.redis = redis.from_url(AuditConfig.REDIS_URL, decode_responses=True)
        self.stream = AuditConfig.STREAM_NAME

    def read(self, last_id="0-0"):
        return self.redis.xread({self.stream: last_id}, block=5000)