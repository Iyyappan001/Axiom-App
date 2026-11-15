"""Composition root for the modular monolith."""

from typing import Any


def create_app() -> Any:
    """Create the Kivy application lazily so domain tests need no GUI runtime."""
    from kivy.app import App

    from app.core.app_state import create_demo_state
    from app.ui.app_shell import Dashboard

    class LifeOSApp(App):
        title = "LifeOS"

        def build(self):
            # Replace the demo factory with repository-backed loading in the persistence step.
            return Dashboard(state=create_demo_state())

    return LifeOSApp()
