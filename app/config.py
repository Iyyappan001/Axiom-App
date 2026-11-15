"""Application configuration with safe development defaults."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    environment: str = "development"
    auto_lock_seconds: int = 120
    price_updates_enabled: bool = False
