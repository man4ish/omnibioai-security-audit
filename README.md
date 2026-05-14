# OmniBioAI Security Audit System

A high-performance, Redis Streams–based audit logging and event streaming system for the OmniBioAI ecosystem. It provides **zero-trust observability**, **HPC-safe audit trails**, and **real-time security event processing** across distributed services.

---

## Overview

The audit system captures and streams security-relevant events from:

* Authentication service
* IAM client (token validation, cache hits/misses)
* Policy engine (RBAC/ABAC decisions)
* Workflow execution (TES, HPC jobs)
* Control plane operations

It is designed for:

* Sub-millisecond logging overhead
* Distributed microservices
* HPC-scale workloads
* Zero-trust architectures

---

## Architecture

```
Services (Auth / IAM / Policy / TES)
            │
            ▼
     Audit Logger (async)
            │
            ▼
   Redis Streams (audit:events)
            │
    ┌───────┴────────┐
    ▼                ▼
Stream Consumers   Future Sink Layer
(processors)       (DB / S3 / OpenSearch)
```

---

## Key Features

### 🚀 High Performance

* Async non-blocking logging
* Redis Streams backbone
* Minimal overhead on critical paths

### 🔐 Zero Trust Observability

* Every decision is logged
* Full traceability of:

  * user actions
  * policy decisions
  * system events

### 🧬 HPC-Aware Design

* Safe for large-scale distributed compute
* Designed for workflow engines like TES
* Handles thousands of concurrent events

### 📡 Real-time Streaming

* Redis Streams allow replayable audit logs
* Consumer pipeline ready for scaling

---

## Event Types

Common events tracked:

* `auth_login`
* `auth_failed`
* `iam_cache_hit`
* `iam_cache_miss`
* `policy_decision`
* `tes_submit`
* `tes_complete`

---

## Installation

```bash
pip install redis pydantic fastapi
```

---

## Environment Variables

```bash
REDIS_URL=redis://localhost:6379
AUDIT_STREAM=audit:events
SERVICE_NAME=omnibioai-service
AUDIT_MAXLEN=1000000
```

---

## Usage

### Initialize Logger

```python
from audit.logger import AuditLogger
from audit.models import AuditEvent
from audit.config import AuditConfig

logger = AuditLogger()
```

---

### Log an Event

```python
await logger.log(
    AuditEvent(
        service="auth-service",
        event_type="auth_login",
        user_id="user_123",
        action="login",
        decision="success",
    )
)
```

---

## FastAPI Integration

```python
from fastapi import APIRouter
from audit.logger import AuditLogger

router = APIRouter()
logger = AuditLogger()

@router.post("/login")
async def login():
    await logger.log(...)
```

---

## Stream Consumer

Read audit events:

```python
from consumers.stream_reader import StreamReader

reader = StreamReader()

data = reader.read()
print(data)
```

---

## Consumer Pipeline

You can extend consumers for:

* anomaly detection
* security alerts
* analytics dashboards
* compliance reporting

---

## Design Principles

### 1. Never block core execution

Audit failure must NOT break system flow.

### 2. Append-only logs

Redis Streams ensure immutable audit history.

### 3. Distributed-first

Works across:

* local dev
* HPC clusters
* cloud microservices

### 4. Traceability-first design

Every event supports:

* trace_id
* user_id
* service context

---

## Integration with OmniBioAI Ecosystem

This service integrates with:

* omnibioai-auth
* omnibioai-iam-client
* omnibioai-policy-engine

---

## Future Extensions

Planned enhancements:

* OpenSearch / PostgreSQL sink
* Real-time security dashboard
* AI-based anomaly detection
* Policy decision graph visualization
* Compliance reporting engine

---

## License

MIT (or your organization license)

