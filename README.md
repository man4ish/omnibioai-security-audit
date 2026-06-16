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

## Running

### Via OmniBioAI Studio (recommended)

```bash
cd ~/Desktop/machine/omnibioai-studio
docker compose up -d security-audit
```

Access (internal only):
`http://security-audit:8004` (Docker internal network)

### Health check

```bash
curl http://localhost:8004/health
# {"status": "ok"}
```

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://redis:6379` | Redis Streams backend |
| `AUDIT_STREAM` | `audit:events` | Stream name |
| `SERVICE_NAME` | `omnibioai-security-audit` | Service identifier |
| `AUDIT_MAXLEN` | `1000000` | Max stream length |

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

## Testing

```bash
cd ~/Desktop/machine/omnibioai-security-audit
pytest tests/ -v --cov=.

# 99% coverage
# Covers: audit logger, stream reader, decorators,
#         context management, event types
```

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

## Roadmap

| Feature | Status |
|---------|--------|
| Redis Streams audit backbone | ✓ Stable |
| Async non-blocking logging | ✓ Stable |
| Fail-open design | ✓ Stable |
| Distributed trace ID support | ✓ Stable |
| 99% test coverage | ✓ Stable |
| OpenSearch / PostgreSQL sink | Planned |
| Real-time security dashboard | Planned |
| AI-based anomaly detection | Planned v0.5 |
| Compliance reporting engine | Planned v0.5 |

---

## Related Services

| Service | Role |
|---------|------|
| `omnibioai-api-gateway` | Fires audit events on every request |
| `omnibioai-auth` | Fires auth_login / auth_failed events |
| `omnibioai-policy-engine` | Fires policy_decision events |
| `omnibioai-iam-client` | Fires iam_cache_hit / iam_cache_miss events |
| `omnibioai-security-sdk` | Provides fire_audit() helper used by all services |
| `omnibioai-studio` | Manages security-audit container lifecycle |

---

## License

Apache 2.0

