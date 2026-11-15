import pytest

from app.core.app_state import create_demo_state
from app.modules.productivity.service import complete_task


def test_completing_task_awards_xp_once() -> None:
    state = create_demo_state()

    awarded = complete_task(state, "task-1")

    assert awarded == 55
    assert state.xp_total == 55
    assert state.tasks[0].completed is True
    assert complete_task(state, "task-1") == 0
    assert state.xp_total == 55


def test_unknown_task_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown task"):
        complete_task(create_demo_state(), "missing")
