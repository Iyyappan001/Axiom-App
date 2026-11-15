from decimal import Decimal

from app.core.app_state import GoalState, create_demo_state


def test_demo_state_exposes_dashboard_metrics() -> None:
    state = create_demo_state()

    assert state.completed_tasks == 1
    assert state.completed_habits == 3
    assert state.wealth.net_worth == Decimal("1248000")


def test_goal_progress_is_bounded() -> None:
    goal = GoalState("goal", "Example", Decimal("12"), Decimal("10"))

    assert goal.progress_percent == 100
