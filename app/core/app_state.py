"""In-memory application state for the first data-driven UI slice.

This state is deliberately separate from Kivy widgets. The next persistence
step can replace the demo factory with repository-backed loading without
rewriting the dashboard layout.
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class TaskState:
    id: str
    title: str
    completed: bool
    priority: str
    difficulty: int = 3
    importance: int = 3
    xp_awarded: int = 0


@dataclass
class HabitState:
    id: str
    name: str
    completed: bool
    streak_days: int


@dataclass
class GoalState:
    id: str
    title: str
    current: Decimal
    target: Decimal

    @property
    def progress_percent(self) -> int:
        if self.target <= 0:
            return 0
        return min(100, round(float(self.current / self.target) * 100))


@dataclass
class WealthState:
    net_worth: Decimal
    assets: Decimal
    liabilities: Decimal
    investments: Decimal
    monthly_change_percent: Decimal
    monthly_expenses: Decimal


@dataclass
class DashboardState:
    user_name: str
    date_label: str
    tasks: list[TaskState]
    habits: list[HabitState]
    goals: list[GoalState]
    wealth: WealthState
    xp_total: int = 0

    @property
    def completed_tasks(self) -> int:
        return sum(task.completed for task in self.tasks)

    @property
    def completed_habits(self) -> int:
        return sum(habit.completed for habit in self.habits)

    @property
    def completed_goals(self) -> int:
        return sum(goal.progress_percent >= 100 for goal in self.goals)

    @property
    def progress_percent(self) -> int:
        total = len(self.tasks) + len(self.habits) + len(self.goals)
        completed = self.completed_tasks + self.completed_habits + self.completed_goals
        return round(completed / total * 100) if total else 0


def create_demo_state() -> DashboardState:
    """Return fictional data for previews until repositories are connected."""
    return DashboardState(
        user_name="Aryan",
        date_label="Saturday, 15 November",
        tasks=[
            TaskState("task-1", "Finish project module", False, "High", 4, 5),
            TaskState("task-2", "Gym / Workout", True, "", 3, 3),
            TaskState("task-3", "Review investments", False, "Medium", 3, 4),
        ],
        habits=[
            HabitState("habit-1", "Gym / Workout", True, 23),
            HabitState("habit-2", "Read (30 min)", True, 18),
            HabitState("habit-3", "Sleep before 11 PM", True, 23),
            HabitState("habit-4", "No junk food", False, 12),
        ],
        goals=[
            GoalState("goal-1", "Build ₹50 Lakh Net Worth", Decimal("1248000"), Decimal("5000000")),
            GoalState("goal-2", "Become Debt Free", Decimal("472000"), Decimal("1000000")),
            GoalState("goal-3", "Health & Fitness", Decimal("92"), Decimal("85")),
        ],
        wealth=WealthState(
            net_worth=Decimal("1248000"),
            assets=Decimal("720000"),
            liabilities=Decimal("472000"),
            investments=Decimal("340000"),
            monthly_change_percent=Decimal("4.8"),
            monthly_expenses=Decimal("48200"),
        ),
    )
