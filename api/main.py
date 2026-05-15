from fastapi import FastAPI

from api.routes_audit import router
from audit.config import AuditConfig

app = FastAPI(title=f"OmniBioAI Security Audit — {AuditConfig.SERVICE_NAME}")

app.include_router(router)
