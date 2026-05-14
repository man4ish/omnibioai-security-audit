import functools
import asyncio
from audit.logger import AuditLogger
from audit.models import AuditEvent
from audit.config import AuditConfig
from audit.context import get_trace_id, get_user_id

logger = AuditLogger()


def audit(event_type: str, action: str):
    def wrapper(func):
        @functools.wraps(func)
        async def async_inner(*args, **kwargs):
            result = await func(*args, **kwargs)

            await logger.log(
                AuditEvent(
                    service=AuditConfig.SERVICE_NAME,
                    event_type=event_type,
                    user_id=get_user_id(),
                    action=action,
                    decision="success",
                    trace_id=get_trace_id(),
                )
            )

            return result

        return async_inner

    return wrapper