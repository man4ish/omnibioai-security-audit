from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid


class AuditEvent(BaseModel):
    event_id: str = str(uuid.uuid4())
    timestamp: datetime = datetime.utcnow()

    service: str
    event_type: str   # auth, iam, policy, tes

    user_id: Optional[str] = None
    action: str = ""
    resource: Optional[str] = None

    decision: Optional[str] = None  # allow / deny / success / fail
    reason: Optional[str] = None

    trace_id: Optional[str] = None
    context: Dict[str, Any] = {}