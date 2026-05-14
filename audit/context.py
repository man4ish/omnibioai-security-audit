from contextvars import ContextVar
from typing import Optional

trace_id_var = ContextVar("trace_id", default=None)
user_id_var = ContextVar("user_id", default=None)


def set_trace_id(trace_id: str):
    trace_id_var.set(trace_id)


def get_trace_id() -> Optional[str]:
    return trace_id_var.get()


def set_user_id(user_id: str):
    user_id_var.set(user_id)


def get_user_id() -> Optional[str]:
    return user_id_var.get()