import json


def process_event(raw_event: str):
    event = json.loads(raw_event)

    # future:
    # - anomaly detection
    # - security alerts
    # - metrics aggregation

    return {
        "user": event.get("user_id"),
        "event": event.get("event_type"),
        "decision": event.get("decision"),
    }