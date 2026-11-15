import pytest

from app.core.app_state import create_demo_state
from app.modules.productivity.service import add_task


def test_add_task_appends_new_task() -> None:
    state = create_demo_state()

    task = add_task(state, "Plan the week", "High", 4, 5)

    assert task.title == "Plan the week"
    assert task.priority == "High"
    assert task.id.startswith("task-")
    assert state.tasks[-1] is task


def test_add_task_rejects_blank_title() -> None:
    with pytest.raises(ValueError, match="title is required"):
        add_task(create_demo_state(), "   ")
