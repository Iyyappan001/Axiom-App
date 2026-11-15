"""Productivity actions for the first interactive task slice."""

from __future__ import annotations

from app.core.app_state import DashboardState, TaskState
from app.data.repositories.task_repository import TaskRepository
from app.modules.productivity.scoring import completion_xp
from uuid import uuid4


def add_task(
    state: DashboardState,
    title: str,
    priority: str = "Medium",
    difficulty: int = 3,
    importance: int = 3,
    repository: TaskRepository | None = None,
) -> TaskState:
    """Add a new task to the current in-memory state."""
    clean_title = title.strip()
    if not clean_title:
        raise ValueError("task title is required")
    if priority not in {"High", "Medium", "Low"}:
        raise ValueError("priority must be High, Medium, or Low")
    if not 1 <= difficulty <= 5 or not 1 <= importance <= 5:
        raise ValueError("difficulty and importance must be between 1 and 5")

    task = TaskState(
        id=f"task-{uuid4().hex}",
        title=clean_title,
        completed=False,
        priority=priority,
        difficulty=difficulty,
        importance=importance,
    )
    state.tasks.append(task)
    if repository:
        repository.save(task)
    return task


def complete_task(state: DashboardState, task_id: str, repository: TaskRepository | None = None) -> int:
    """Complete a task and award XP once.

    A future repository implementation should persist the completion and XP
    ledger entry atomically. Repeated taps are intentionally no-ops.
    """
    task = next((item for item in state.tasks if item.id == task_id), None)
    if task is None:
        raise ValueError(f"unknown task: {task_id}")
    if task.completed:
        return 0

    task.completed = True
    task.xp_awarded = completion_xp(task.difficulty, task.importance)
    state.xp_total += task.xp_awarded
    if repository:
        repository.save(task)
    return task.xp_awarded
