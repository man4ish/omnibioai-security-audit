import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture
def mock_async_redis():
    return AsyncMock()


@pytest.fixture
def mock_sync_redis():
    return MagicMock()


@pytest.fixture
def audit_logger(mock_async_redis):
    with patch("audit.logger.redis") as mock_redis_module:
        mock_redis_module.from_url.return_value = mock_async_redis
        from audit.logger import AuditLogger
        logger = AuditLogger()
        logger.redis = mock_async_redis
        yield logger, mock_async_redis


@pytest.fixture
def stream_reader(mock_sync_redis):
    with patch("consumers.stream_reader.redis") as mock_redis_module:
        mock_redis_module.from_url.return_value = mock_sync_redis
        from consumers.stream_reader import StreamReader
        reader = StreamReader()
        reader.redis = mock_sync_redis
        yield reader, mock_sync_redis
