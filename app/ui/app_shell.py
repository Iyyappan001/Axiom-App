"""Reference-matched Axiom/LifeOS mobile dashboard UI."""

from __future__ import annotations

from collections.abc import Callable

from kivy.graphics import Color, Ellipse, Line, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from app.core.app_state import DashboardState, create_demo_state
from app.data.repositories.task_repository import InMemoryTaskRepository, TaskRepository
from app.modules.productivity.service import add_task, complete_task
from app.ui.theme import ACCENT, BACKGROUND, PRIMARY, SURFACE, TEXT, TEXT_MUTED

GREEN = (0.08, 0.95, 0.48, 1)
GREEN_SOFT = (0.04, 0.37, 0.20, 1)
RED = (1.0, 0.32, 0.35, 1)
AMBER = (1.0, 0.72, 0.12, 1)


class AxiomLabel(Label):
    """Label with predictable wrapping and vertical alignment."""

    def __init__(self, **kwargs):
        super().__init__(halign="left", valign="middle", **kwargs)
        self.bind(size=self._sync_text_size)
        self._sync_text_size()

    def _sync_text_size(self, *_args):
        self.text_size = (self.width, self.height)


def label(text: str, size: int = 13, color=TEXT, bold: bool = False) -> AxiomLabel:
    return AxiomLabel(text=text, color=color, font_size=dp(size), bold=bold)


class Card(BoxLayout):
    """Dark rounded card used throughout the UI."""

    def __init__(self, glow: bool = False, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*SURFACE)
            self.fill = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
            Color(*(GREEN if glow else (0.12, 0.18, 0.20, 1)))
            self.outline = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(15)), width=0.8)
        self.bind(pos=self._sync_canvas, size=self._sync_canvas)

    def _sync_canvas(self, *_args):
        self.fill.pos = self.pos
        self.fill.size = self.size
        self.outline.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(15))


class Chart(Widget):
    """Small neon wealth chart matching the reference card."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._draw, size=self._draw)
        self._draw()

    def _draw(self, *_args):
        x, y, w, h = self.x, self.y, self.width, self.height
        points = [x, y + h * 0.18, x + w * 0.13, y + h * 0.13,
                  x + w * 0.25, y + h * 0.35, x + w * 0.38, y + h * 0.28,
                  x + w * 0.50, y + h * 0.58, x + w * 0.62, y + h * 0.45,
                  x + w * 0.75, y + h * 0.68, x + w * 0.88, y + h * 0.61,
                  x + w, y + h * 0.88]
        with self.canvas:
            self.canvas.clear()
            Color(0.08, 0.95, 0.48, 0.10)
            self.canvas.add(RoundedRectangle(pos=(x, y), size=(w, h * 0.25), radius=[dp(8)]))
            Color(*GREEN)
            self.canvas.add(Line(points=points, width=dp(1.4)))
            self.canvas.add(Ellipse(pos=(x + w - dp(4), y + h * 0.88 - dp(4)), size=(dp(8), dp(8))))


class RingProgress(Widget):
    """Circular progress ring used in the Today section."""

    def __init__(self, value: int = 67, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_args):
        diameter = min(self.width, self.height) - dp(12)
        x = self.center_x - diameter / 2
        y = self.center_y - diameter / 2
        with self.canvas:
            self.canvas.clear()
            Color(0.12, 0.20, 0.22, 1)
            self.canvas.add(Line(ellipse=(x, y, diameter, diameter), width=dp(7)))
            Color(*GREEN)
            self.canvas.add(Line(ellipse=(x, y, diameter, diameter, 0, self.value * 3.6), width=dp(7)))


def button(text: str, callback: Callable | None = None, active: bool = False) -> Button:
    item = Button(text=text, color=BACKGROUND if active else TEXT_MUTED, font_size=dp(11), bold=active,
                  background_normal="", background_color=GREEN if active else (0, 0, 0, 0),
                  size_hint_y=None, height=dp(34))
    if callback:
        item.bind(on_release=callback)
    return item


class Dashboard(BoxLayout):
    """Portrait mobile dashboard with functional reference-style navigation."""

    tabs = ("Home", "Tasks", "Wealth", "Goals", "Insights")

    def __init__(self, state: DashboardState | None = None,
                 task_repository: TaskRepository | None = None, **kwargs):
        super().__init__(orientation="vertical", padding=[dp(14), dp(8)], spacing=dp(7), **kwargs)
        self.state = state or create_demo_state()
        self.task_repository = task_repository or InMemoryTaskRepository(self.state.tasks)
        with self.canvas.before:
            Color(*BACKGROUND)
            self.background = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._sync_background, size=self._sync_background)
        self._header()
        self.scroller = ScrollView(do_scroll_x=False, bar_width=0)
        self.content = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroller.add_widget(self.content)
        self.add_widget(self.scroller)
        self._navigation()
        self.show_tab("Home")

    def _sync_background(self, *_args):
        self.background.pos = self.pos
        self.background.size = self.size

    def _header(self):
        header = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(76), spacing=dp(1))
        brand = BoxLayout(size_hint_y=None, height=dp(38))
        brand.add_widget(label("Λ", 34, GREEN, True))
        brand.add_widget(label("AXIOM", 27, TEXT, True))
        brand.add_widget(Widget())
        brand.add_widget(button("♧"))
        brand.add_widget(button("⋮"))
        header.add_widget(brand)
        header.add_widget(label("LifeOS   ·   Tasks   ·   Wealth   ·   Goals   ·   Insights", 10, TEXT_MUTED))
        self.add_widget(header)

    def _navigation(self):
        nav = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(2))
        self.nav_buttons: dict[str, Button] = {}
        icons = {"Home": "⌂", "Tasks": "☑", "Wealth": "▣", "Goals": "◎", "Insights": "▥"}
        for tab in self.tabs:
            item = Button(text=f"{icons[tab]}\n{tab}", font_size=dp(10), color=TEXT_MUTED,
                          background_normal="", background_color=(0, 0, 0, 0))
            item.bind(on_release=lambda _item, selected=tab: self.show_tab(selected))
            self.nav_buttons[tab] = item
            nav.add_widget(item)
        self.add_widget(nav)

    def show_tab(self, tab: str):
        self.active_tab = tab
        self.content.clear_widgets()
        for name, item in self.nav_buttons.items():
            item.color = GREEN if name == tab else TEXT_MUTED
        {"Home": self._home, "Tasks": self._tasks, "Wealth": self._wealth,
         "Goals": self._goals, "Insights": self._insights}[tab]()

    def _title(self, title: str, subtitle: str, action: Callable | None = None,
               action_text: str = "•••"):
        row = BoxLayout(size_hint_y=None, height=dp(55))
        stack = BoxLayout(orientation="vertical")
        stack.add_widget(label(title, 20, TEXT, True))
        stack.add_widget(label(subtitle, 11, TEXT_MUTED))
        row.add_widget(stack)
        row.add_widget(button(action_text, callback=action, active=action is not None))
        self.content.add_widget(row)

    def _home(self):
        self._title(f"Good morning, {self.state.user_name} 👋", "Let's make progress today.")
        hero = Card(orientation="vertical", padding=dp(15), spacing=dp(2), size_hint_y=None, height=dp(165), glow=True)
        hero.add_widget(label("TODAY'S PROGRESS", 10, TEXT_MUTED, True))
        progress_row = BoxLayout(spacing=dp(10))
        ring = RingProgress(67, size_hint=(None, 1), width=dp(88))
        progress_row.add_widget(ring)
        summary = BoxLayout(orientation="vertical")
        summary.add_widget(label(f"{self.state.progress_percent}%", 27, GREEN, True))
        summary.add_widget(label(f"Tasks                 {self.state.completed_tasks} / {len(self.state.tasks)}", 12, TEXT))
        summary.add_widget(label(f"Habits                {self.state.completed_habits} / {len(self.state.habits)}", 12, TEXT))
        summary.add_widget(label(f"Goals                  {self.state.completed_goals} / {len(self.state.goals)}", 12, TEXT))
        summary.add_widget(label(f"XP earned              {self.state.xp_total}", 12, GREEN))
        progress_row.add_widget(summary)
        hero.add_widget(progress_row)
        self.content.add_widget(hero)
        self._wealth_card()
        self._tasks_card()
        self._habits_card()

    def _wealth_card(self):
        card = Card(orientation="vertical", padding=dp(14), spacing=dp(2), size_hint_y=None, height=dp(210))
        top = BoxLayout(size_hint_y=None, height=dp(40))
        top.add_widget(label("WEALTH SNAPSHOT", 10, TEXT_MUTED, True))
        top.add_widget(label(f"↗ +{self.state.wealth.monthly_change_percent}%", 12, GREEN, True))
        card.add_widget(top)
        card.add_widget(label(f"₹{self._money(self.state.wealth.net_worth)}", 26, TEXT, True))
        card.add_widget(label("Net Worth", 11, TEXT_MUTED))
        card.add_widget(Chart(size_hint_y=None, height=dp(72)))
        row = GridLayout(cols=2, size_hint_y=None, height=dp(38), spacing=dp(10))
        row.add_widget(label(f"▣  Assets     ₹{self._money(self.state.wealth.assets)}", 11, TEXT_MUTED))
        row.add_widget(label(f"▣  Liabilities     ₹{self._money(self.state.wealth.liabilities)}", 11, TEXT_MUTED))
        card.add_widget(row)
        self.content.add_widget(card)

    def _tasks_card(self):
        card = Card(orientation="vertical", padding=dp(14), spacing=dp(1), size_hint_y=None, height=dp(162))
        heading = BoxLayout(size_hint_y=None, height=dp(30))
        heading.add_widget(label("TODAY'S TOP TASKS", 10, TEXT_MUTED, True))
        heading.add_widget(label("View All", 11, GREEN, True))
        card.add_widget(heading)
        for task in self.state.tasks:
            row = BoxLayout(size_hint_y=None, height=dp(38), spacing=dp(6))
            checkbox = Button(text="✓" if task.completed else "□", font_size=dp(18),
                              color=GREEN if task.completed else TEXT_MUTED,
                              background_normal="", background_color=(0, 0, 0, 0),
                              size_hint=(None, 1), width=dp(28))
            checkbox.bind(on_release=lambda _button, task_id=task.id: self._complete_task(task_id))
            row.add_widget(checkbox)
            row.add_widget(label(task.title, 12, TEXT))
            if task.priority:
                row.add_widget(label(task.priority, 10,
                                     RED if task.priority == "High" else AMBER, True))
            card.add_widget(row)
        self.content.add_widget(card)

    def _habits_card(self):
        card = Card(orientation="vertical", padding=dp(14), spacing=dp(4), size_hint_y=None, height=dp(132))
        card.add_widget(label(f"HABITS  {self.state.completed_habits}/{len(self.state.habits)}", 10, TEXT_MUTED, True))
        for habit in self.state.habits[:3]:
            row = BoxLayout(size_hint_y=None, height=dp(27))
            row.add_widget(label(("✓   " if habit.completed else "□   ") + habit.name, 12, TEXT))
            row.add_widget(label("🔥 " + str(habit.streak_days) + "d", 11, AMBER, True))
            card.add_widget(row)
        self.content.add_widget(card)

    def _tasks(self):
        self._title("Tasks", "Plan, track & build habits", self._open_task_editor, "+ Add")
        self._filters(("Today⌄", "All", "Tasks", "Habits"))
        self._tasks_card()
        self._habits_card()

    def _wealth(self):
        self._title("Wealth", "Money, loans, investments & net worth")
        self._wealth_card()
        self._stat_grid()

    def _goals(self):
        self._title("Goals", "Long-term targets with visible progress")
        for goal in self.state.goals:
            card = Card(orientation="vertical", padding=dp(14), spacing=dp(4), size_hint_y=None, height=dp(105))
            card.add_widget(label(goal.title, 13, TEXT, True))
            card.add_widget(label(f"₹{self._money(goal.current)} / ₹{self._money(goal.target)}", 11, TEXT_MUTED))
            card.add_widget(ProgressBar(max=100, value=goal.progress_percent,
                                        size_hint_y=None, height=dp(8)))
            self.content.add_widget(card)

    def _insights(self):
        self._title("Insights", "Trends, reports & personal growth")
        self._stat_grid()
        card = Card(orientation="vertical", padding=dp(14), spacing=dp(5), size_hint_y=None, height=dp(142))
        card.add_widget(label("KEY TAKEAWAYS", 10, TEXT_MUTED, True))
        for text in ("Wealth grew by 4.8% this month.", "Task completion is up by 12%.", "Habit consistency is at 83%."):
            card.add_widget(label("•  " + text, 12, TEXT))
        self.content.add_widget(card)

    def _stat_grid(self):
        grid = GridLayout(cols=2, spacing=dp(9), size_hint_y=None, height=dp(142))
        grid.add_widget(self._stat("ASSETS", f"₹{self._money(self.state.wealth.assets)}", GREEN))
        grid.add_widget(self._stat("LIABILITIES", f"₹{self._money(self.state.wealth.liabilities)}", RED))
        grid.add_widget(self._stat("INVESTMENTS", f"₹{self._money(self.state.wealth.investments)}", PRIMARY))
        grid.add_widget(self._stat("EXPENSES", f"₹{self._money(self.state.wealth.monthly_expenses)}", ACCENT))
        self.content.add_widget(grid)

    @staticmethod
    def _stat(title: str, value: str, color) -> Card:
        card = Card(orientation="vertical", padding=dp(12), spacing=dp(2))
        card.add_widget(label(title, 10, TEXT_MUTED, True))
        card.add_widget(label(value, 18, color, True))
        card.add_widget(label("This month", 10, TEXT_MUTED))
        return card

    def _filters(self, values: tuple[str, ...]):
        row = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(5))
        for index, value in enumerate(values):
            row.add_widget(button(value, active=index == 0))
        self.content.add_widget(row)

    def _complete_task(self, task_id: str):
        complete_task(self.state, task_id, self.task_repository)
        self.show_tab(self.active_tab)

    def _open_task_editor(self, *_args):
        form = BoxLayout(orientation="vertical", padding=dp(18), spacing=dp(10))
        title_input = TextInput(hint_text="Task title", multiline=False, size_hint_y=None, height=dp(44))
        priority_input = Spinner(text="Medium", values=("High", "Medium", "Low"),
                                 size_hint_y=None, height=dp(44))
        difficulty_input = Spinner(text="Difficulty 3", values=tuple(f"Difficulty {value}" for value in range(1, 6)),
                                   size_hint_y=None, height=dp(44))
        importance_input = Spinner(text="Importance 3", values=tuple(f"Importance {value}" for value in range(1, 6)),
                                   size_hint_y=None, height=dp(44))
        form.add_widget(label("NEW TASK", 12, GREEN, True))
        form.add_widget(title_input)
        form.add_widget(priority_input)
        form.add_widget(difficulty_input)
        form.add_widget(importance_input)
        feedback = label("", 11, RED)
        form.add_widget(feedback)
        actions = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8))
        popup = Popup(title="Add task", content=form, size_hint=(0.9, None), height=dp(390),
                      separator_color=GREEN)
        cancel = button("Cancel")
        cancel.bind(on_release=popup.dismiss)
        save = button("Save task", active=True)

        def save_task(_button):
            try:
                difficulty = int(difficulty_input.text.rsplit(" ", 1)[-1])
                importance = int(importance_input.text.rsplit(" ", 1)[-1])
                add_task(self.state, title_input.text, priority_input.text, difficulty, importance,
                         self.task_repository)
            except ValueError as error:
                feedback.text = str(error)
                return
            popup.dismiss()
            self.show_tab("Tasks")

        save.bind(on_release=save_task)
        actions.add_widget(cancel)
        actions.add_widget(save)
        form.add_widget(actions)
        popup.open()

    @staticmethod
    def _money(value) -> str:
        return f"{value:,.0f}"
