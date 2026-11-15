"""Task repository boundary.

The production implementation should receive an opened SQLCipher-compatible
connection. Keeping the boundary here lets the Kivy UI remain independent of
the storage driver and makes migrations testable before Android packaging.
"""

from collections.abc import Iterable
from dataclasses import replace
from typing import Protocol

from app.core.app_state import TaskState


class TaskRepository(Protocol):
    def list_tasks(self) -> list[TaskState]: ...

    def save(self, task: TaskState) -> None: ...


class InMemoryTaskRepository:
    """Safe preview repository used until the encrypted adapter is wired."""

    def __init__(self, tasks: Iterable[TaskState] = ()):
        self._tasks = {task.id: replace(task) for task in tasks}

    def list_tasks(self) -> list[TaskState]:
        return [replace(task) for task in self._tasks.values()]

    def save(self, task: TaskState) -> None:
        self._tasks[task.id] = replace(task)
