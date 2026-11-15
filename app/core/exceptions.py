"""Application-level exception types."""


class LifeOSError(Exception):
    """Base exception for expected application failures."""


class ValidationError(LifeOSError):
    """Raised when user input violates a domain invariant."""
