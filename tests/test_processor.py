import json
import pytest
from consumers.processor import process_event
from consumers.sink import Sink


# ---------------------------------------------------------------------------
# process_event
# ---------------------------------------------------------------------------

def test_process_event_extracts_user_id():
    raw = json.dumps({"user_id": "u1", "event_type": "auth_login", "decision": "allow"})
    result = process_event(raw)
    assert result["user"] == "u1"


def test_process_event_extracts_event_type():
    raw = json.dumps({"user_id": "u1", "event_type": "policy_decision", "decision": "deny"})
    result = process_event(raw)
    assert result["event"] == "policy_decision"


def test_process_event_extracts_decision():
    raw = json.dumps({"user_id": "u1", "event_type": "test", "decision": "success"})
    result = process_event(raw)
    assert result["decision"] == "success"


def test_process_event_missing_fields_return_none():
    raw = json.dumps({})
    result = process_event(raw)
    assert result["user"] is None
    assert result["event"] is None
    assert result["decision"] is None


def test_process_event_partial_fields():
    raw = json.dumps({"user_id": "u2"})
    result = process_event(raw)
    assert result["user"] == "u2"
    assert result["event"] is None


def test_process_event_raises_on_invalid_json():
    with pytest.raises(json.JSONDecodeError):
        process_event("not-json")


def test_process_event_returns_dict():
    raw = json.dumps({"user_id": "u3", "event_type": "test", "decision": "ok"})
    result = process_event(raw)
    assert isinstance(result, dict)
    assert set(result.keys()) == {"user", "event", "decision"}


# ---------------------------------------------------------------------------
# Sink
# ---------------------------------------------------------------------------

def test_sink_write_does_not_raise():
    sink = Sink()
    # write prints to stdout — just verify no exception
    sink.write({"user": "u1", "event": "test"})


def test_sink_write_accepts_any_dict():
    sink = Sink()
    sink.write({})
    sink.write({"nested": {"key": "value"}})
