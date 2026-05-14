import json
import redis.asyncio as redis
from typing import Optional
from audit.config import AuditConfig
from audit.models import AuditEvent


class AuditLogger:
    def __init__(self):
        self.redis = redis.from_url(AuditConfig.REDIS_URL, decode_responses=True)

    async def log(self, event: AuditEvent):
        payload = event.dict()

        try:
            await self.redis.xadd(
                AuditConfig.STREAM_NAME,
                {"data": json.dumps(payload)},
                maxlen=AuditConfig.MAX_STREAM_LENGTH,
                approximate=True,
            )
        except Exception as e:
            # NEVER break core system
            print(f"[AUDIT ERROR] {e}")