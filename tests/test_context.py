import pytest
from audit.context import (
    set_trace_id, get_trace_id,
    set_user_id, get_user_id,
    trace_id_var, user_id_var,
)
from audit.contexts import inject_context


# ---------------------------------------------------------------------------
# trace_id context var
# ---------------------------------------------------------------------------

def test_trace_id_default_is_none():
    # Reset to default
    token = trace_id_var.set(None)
    try:
        assert get_trace_id() is None
    finally:
        trace_id_var.reset(token)


def test_set_and_get_trace_id():
    token = trace_id_var.set(None)
    try:
        set_trace_id("trace-abc-123")
        assert get_trace_id() == "trace-abc-123"
    finally:
        trace_id_var.reset(token)


def test_trace_id_can_be_overwritten():
    token = trace_id_var.set(None)
    try:
        set_trace_id("first")
        set_trace_id("second")
        assert get_trace_id() == "second"
    finally:
        trace_id_var.reset(token)


# ---------------------------------------------------------------------------
# user_id context var
# ---------------------------------------------------------------------------

def test_user_id_default_is_none():
    token = user_id_var.set(None)
    try:
        assert get_user_id() is None
    finally:
        user_id_var.reset(token)


def test_set_and_get_user_id():
    token = user_id_var.set(None)
    try:
        set_user_id("user-xyz")
        assert get_user_id() == "user-xyz"
    finally:
        user_id_var.reset(token)


def test_user_id_can_be_overwritten():
    token = user_id_var.set(None)
    try:
        set_user_id("user1")
        set_user_id("user2")
        assert get_user_id() == "user2"
    finally:
        user_id_var.reset(token)


# ---------------------------------------------------------------------------
# inject_context (contexts.py)
# ---------------------------------------------------------------------------

def test_inject_context_sets_trace_id():
    token_t = trace_id_var.set(None)
    token_u = user_id_var.set(None)
    try:
        trace_id = inject_context(user_id="u1")
        assert get_trace_id() == trace_id
        assert len(trace_id) == 36  # UUID4 format
    finally:
        trace_id_var.reset(token_t)
        user_id_var.reset(token_u)


def test_inject_context_sets_user_id():
    token_t = trace_id_var.set(None)
    token_u = user_id_var.set(None)
    try:
        inject_context(user_id="user-99")
        assert get_user_id() == "user-99"
    finally:
        trace_id_var.reset(token_t)
        user_id_var.reset(token_u)


def test_inject_context_returns_uuid_string():
    trace_id = inject_context()
    assert isinstance(trace_id, str)
    assert len(trace_id) == 36


def test_inject_context_generates_unique_trace_ids():
    t1 = inject_context()
    t2 = inject_context()
    assert t1 != t2


def test_inject_context_without_user_id():
    token_u = user_id_var.set(None)
    try:
        inject_context()
        assert get_user_id() is None
    finally:
        user_id_var.reset(token_u)
