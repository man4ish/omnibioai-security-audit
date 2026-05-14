import os


class AuditConfig:
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    STREAM_NAME = os.getenv("AUDIT_STREAM", "audit:events")
    SERVICE_NAME = os.getenv("SERVICE_NAME", "unknown-service")
    MAX_STREAM_LENGTH = int(os.getenv("AUDIT_MAXLEN", "1000000"))