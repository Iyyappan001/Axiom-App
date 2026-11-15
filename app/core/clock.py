"""Time abstraction used by domain services and deterministic tests."""

from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
