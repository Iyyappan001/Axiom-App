"""Redacted logging boundary for security-sensitive application code."""

SENSITIVE_FIELDS = frozenset({"balance", "amount", "account_id", "key", "token", "password"})
