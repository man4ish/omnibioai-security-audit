import pytest
from unittest.mock import MagicMock, patch
from audit.config import AuditConfig


# ---------------------------------------------------------------------------
# StreamReader.read()
# ---------------------------------------------------------------------------

def test_stream_reader_calls_xread(stream_reader):
    reader, mock_redis = stream_reader
    mock_redis.xread.return_value = [("audit:events", [("1-0", {"data": "{}"})])]

    result = reader.read(last_id="0-0")

    mock_redis.xread.assert_called_once_with(
        {AuditConfig.STREAM_NAME: "0-0"}, block=5000
    )
    assert result is not None


def test_stream_reader_default_last_id(stream_reader):
    reader, mock_redis = stream_reader
    mock_redis.xread.return_value = []

    reader.read()

    call_args = mock_redis.xread.call_args[0][0]
    assert "0-0" in call_args.values()


def test_stream_reader_passes_custom_last_id(stream_reader):
    reader, mock_redis = stream_reader
    mock_redis.xread.return_value = []

    reader.read(last_id="1234-5")

    call_args = mock_redis.xread.call_args[0][0]
    assert "1234-5" in call_args.values()


def test_stream_reader_returns_empty_on_timeout(stream_reader):
    reader, mock_redis = stream_reader
    mock_redis.xread.return_value = []

    result = reader.read()

    assert result == []


def test_stream_reader_uses_config_stream_name(stream_reader):
    reader, mock_redis = stream_reader
    mock_redis.xread.return_value = []

    reader.read()

    call_args = mock_redis.xread.call_args[0][0]
    assert AuditConfig.STREAM_NAME in call_args


def test_stream_reader_returns_multiple_entries(stream_reader):
    reader, mock_redis = stream_reader
    entries = [
        ("0-1", {"data": '{"event_type": "auth_login"}'}),
        ("0-2", {"data": '{"event_type": "auth_failed"}'}),
    ]
    mock_redis.xread.return_value = [(AuditConfig.STREAM_NAME, entries)]

    result = reader.read()

    assert len(result) == 1
    assert len(result[0][1]) == 2
