import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    mock_redis = AsyncMock()
    mock_redis.xadd = AsyncMock()

    with patch("audit.logger.redis") as mock_redis_module:
        mock_redis_module.from_url.return_value = mock_redis
        from api.main import app
        tc = TestClient(app)
        # Patch the logger instance on the routes module
        with patch("api.routes_audit.logger") as mock_logger:
            mock_logger.log = AsyncMock()
            yield tc, mock_logger


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------

def test_health_returns_ok(client):
    tc, _ = client
    response = tc.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# GET /audit/test
# ---------------------------------------------------------------------------

def test_audit_test_returns_logged_true(client):
    tc, mock_logger = client
    response = tc.get("/audit/test")
    assert response.status_code == 200
    assert response.json() == {"logged": True}


def test_audit_test_calls_logger_log(client):
    tc, mock_logger = client
    tc.get("/audit/test")
    mock_logger.log.assert_called_once()


def test_audit_test_logs_correct_event_type(client):
    tc, mock_logger = client
    tc.get("/audit/test")
    event = mock_logger.log.call_args[0][0]
    assert event.event_type == "test"
    assert event.action == "health_check"
    assert event.decision == "success"
