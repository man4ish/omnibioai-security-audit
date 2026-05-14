from fastapi import APIRouter
from audit.logger import AuditLogger

router = APIRouter()
logger = AuditLogger()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/audit/test")
async def test_log():
    from audit.models import AuditEvent
    from audit.config import AuditConfig

    await logger.log(
        AuditEvent(
            service=AuditConfig.SERVICE_NAME,
            event_type="test",
            action="health_check",
            decision="success",
        )
    )

    return {"logged": True}