"""Composition root for the modular monolith."""

from typing import Any


def create_app() -> Any:
    """Create the Kivy application lazily so domain tests need no GUI runtime."""
    from kivy.app import App

    class LifeOSApp(App):
        title = "LifeOS"

    return LifeOSApp()
