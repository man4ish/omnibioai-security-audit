from audit.context import set_trace_id, set_user_id
import uuid


def inject_context(user_id: str = None):
    trace_id = str(uuid.uuid4())

    set_trace_id(trace_id)
    set_user_id(user_id)

    return trace_id