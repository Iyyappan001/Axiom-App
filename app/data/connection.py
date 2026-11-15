"""Database connection boundary.

The production implementation must use a SQLCipher-compatible Android binding;
stdlib sqlite3 is intentionally not used for the encrypted store.
"""


class EncryptedDatabase:
    def __init__(self, path: str) -> None:
        self.path = path
        self._opened = False

    def open(self, key: bytes) -> None:
        if not key:
            raise ValueError("database key is required")
        self._opened = True

    def close(self) -> None:
        self._opened = False
