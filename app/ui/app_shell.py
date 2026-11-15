"""AXIOM mobile dashboard presentation layer."""

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

GREEN = PRIMARY
RED = (1.0, 0.30, 0.32, 1)


class AxiomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(halign="left", valign="middle", **kwargs)
        self.bind(size=self._sync_text_size)
        self._sync_text_size()

    def _sync_text_size(self, *_args):
        self.text_size = (self.width, self.height)


def label(text: str, size: int = 13, color=TEXT, bold: bool = False) -> AxiomLabel:
    return AxiomLabel(text=text, color=color, font_size=dp(size), bold=bold)


class AxiomLogo(Widget):
    """Angular AXIOM mark, drawn as vectors so it stays crisp on Android."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_args):
        x, y, w, h = self.x, self.y, self.width, self.height
        with self.canvas:
            self.canvas.clear()
            Color(*GREEN)
            self.canvas.add(Line(points=[x + w*.08, y + h*.12, x + w*.50, y + h*.92,
                                         x + w*.92, y + h*.12], width=dp(3.5)))
            self.canvas.add(Line(points=[x + w*.33, y + h*.43, x + w*.67, y + h*.43], width=dp(3.5)))


class Card(BoxLayout):
    def __init__(self, glow: bool = False, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*SURFACE)
            self.fill = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
            Color(*(GREEN if glow else (0.09, 0.20, 0.19, 1)))
            self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(12)), width=.75)
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *_args):
        self.fill.pos, self.fill.size = self.pos, self.size
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(12))


class Chart(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_args):
        x, y, w, h = self.x, self.y, self.width, self.height
        points = [x, y+h*.15, x+w*.11, y+h*.06, x+w*.22, y+h*.34, x+w*.35, y+h*.27,
                  x+w*.48, y+h*.55, x+w*.63, y+h*.42, x+w*.75, y+h*.68, x+w*.88, y+h*.60, x+w, y+h*.88]
        with self.canvas:
            self.canvas.clear()
            Color(.08, .95, .48, .11)
            self.canvas.add(RoundedRectangle(pos=(x, y), size=(w, h*.32), radius=[dp(8)]))
            Color(*GREEN)
            self.canvas.add(Line(points=points, width=dp(1.25), joint="round"))
            self.canvas.add(Ellipse(pos=(x+w-dp(4), y+h*.88-dp(4)), size=(dp(8), dp(8))))


class RingProgress(Widget):
    def __init__(self, value: int = 67, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_args):
        diameter = max(1, min(self.width, self.height) - dp(12))
        x, y = self.center_x - diameter/2, self.center_y - diameter/2
        with self.canvas:
            self.canvas.clear()
            Color(.12, .24, .23, 1)
            self.canvas.add(Line(ellipse=(x, y, diameter, diameter), width=dp(7)))
            Color(*GREEN)
            self.canvas.add(Line(ellipse=(x, y, diameter, diameter, 0, self.value*3.6), width=dp(7)))


class AxiomButton(Button):
    def __init__(self, active: bool = False, **kwargs):
        self.active = active
        super().__init__(background_normal="", background_down="", **kwargs)
        self.color = BACKGROUND if active else TEXT_MUTED


def button(text: str, callback: Callable | None = None, active: bool = False) -> AxiomButton:
    item = AxiomButton(text=text, active=active, font_size=dp(11), bold=active,
                       size_hint_y=None, height=dp(32))
    if callback:
        item.bind(on_release=callback)
    return item


class Dashboard(BoxLayout):
    tabs = ("Home", "Tasks", "Wealth", "Goals", "Insights")
    icons = {"Home": "⌂", "Tasks": "☑", "Wealth": "▣", "Goals": "◎", "Insights": "▥"}

    def __init__(self, state: DashboardState | None = None,
                 task_repository: TaskRepository | None = None, **kwargs):
        super().__init__(orientation="vertical", padding=[dp(12), dp(8), dp(12), dp(5)], spacing=dp(5), **kwargs)
        self.state = state or create_demo_state()
        self.task_repository = task_repository or InMemoryTaskRepository(self.state.tasks)
        with self.canvas.before:
            Color(*BACKGROUND)
            self.background = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._sync_background, size=self._sync_background)
        self._header()
        self.scroller = ScrollView(do_scroll_x=False, bar_width=0)
        self.content = BoxLayout(orientation="vertical", spacing=dp(9), size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroller.add_widget(self.content)
        self.add_widget(self.scroller)
        self._navigation()
        self.show_tab("Home")

    def _sync_background(self, *_args):
        self.background.pos, self.background.size = self.pos, self.size

    def _header(self):
        header = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(74))
        brand = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
        brand.add_widget(AxiomLogo(size_hint_x=None, width=dp(34)))
        brand.add_widget(label("AXIOM", 25, TEXT, True))
        brand.add_widget(Widget())
        brand.add_widget(label("♧", 20, TEXT_MUTED))
        brand.add_widget(label("⋮", 21, TEXT_MUTED, True))
        header.add_widget(brand)
        header.add_widget(label("LifeOS  ·  Tasks  ·  Wealth  ·  Goals  ·  Insights", 10, TEXT_MUTED))
        self.add_widget(header)

    def _navigation(self):
        nav = BoxLayout(size_hint_y=None, height=dp(57))
        self.nav_buttons: dict[str, AxiomButton] = {}
        for tab in self.tabs:
            item = AxiomButton(text=f"{self.icons[tab]}\n{tab}", font_size=dp(10))
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

    def _title(self, title: str, subtitle: str, action: Callable | None = None, action_text: str = "⋮"):
        row = BoxLayout(size_hint_y=None, height=dp(54))
        stack = BoxLayout(orientation="vertical")
        stack.add_widget(label(title, 19, TEXT, True))
        stack.add_widget(label(subtitle, 10, TEXT_MUTED))
        row.add_widget(stack)
        row.add_widget(button(action_text, callback=action))
        self.content.add_widget(row)

    def _home(self):
        self._title(f"Good Morning,\n{self.state.user_name} 👋", "Let's make progress today.")
        hero = Card(orientation="vertical", padding=dp(13), size_hint_y=None, height=dp(145), glow=True)
        hero.add_widget(label("TODAY'S PROGRESS", 9, TEXT_MUTED, True))
        row = BoxLayout(spacing=dp(8))
        row.add_widget(RingProgress(self.state.progress_percent, size_hint=(None, 1), width=dp(82)))
        summary = BoxLayout(orientation="vertical")
        summary.add_widget(label(f"{self.state.progress_percent}%", 25, GREEN, True))
        summary.add_widget(label(f"◉  Tasks                 {self.state.completed_tasks} / {len(self.state.tasks)}", 11))
        summary.add_widget(label(f"♡  Habits                {self.state.completed_habits} / {len(self.state.habits)}", 11))
        summary.add_widget(label(f"◎  Goals                  {self.state.completed_goals} / {len(self.state.goals)}", 11))
        row.add_widget(summary)
        hero.add_widget(row)
        self.content.add_widget(hero)
        self._wealth_card(); self._tasks_card(); self._habits_card()

    def _wealth_card(self):
        card = Card(orientation="vertical", padding=dp(13), size_hint_y=None, height=dp(195))
        top = BoxLayout(size_hint_y=None, height=dp(28))
        top.add_widget(label("WEALTH SNAPSHOT", 9, TEXT_MUTED, True))
        top.add_widget(label(f"↗ +{self.state.wealth.monthly_change_percent}%", 11, GREEN, True))
        card.add_widget(top)
        card.add_widget(label(f"₹{self._money(self.state.wealth.net_worth)}", 24, TEXT, True))
        card.add_widget(label("Net Worth", 10, TEXT_MUTED))
        card.add_widget(Chart(size_hint_y=None, height=dp(64)))
        row = GridLayout(cols=2, size_hint_y=None, height=dp(36))
        row.add_widget(label(f"▣  Assets\n₹{self._money(self.state.wealth.assets)}", 10, TEXT_MUTED))
        row.add_widget(label(f"▣  Liabilities\n₹{self._money(self.state.wealth.liabilities)}", 10, TEXT_MUTED))
        card.add_widget(row)
        self.content.add_widget(card)

    def _tasks_card(self):
        card = Card(orientation="vertical", padding=dp(13), size_hint_y=None, height=dp(150))
        heading = BoxLayout(size_hint_y=None, height=dp(27))
        heading.add_widget(label("TODAY'S TOP TASKS", 9, TEXT_MUTED, True))
        heading.add_widget(label("View All", 10, GREEN, True))
        card.add_widget(heading)
        for task in self.state.tasks[:3]:
            row = BoxLayout(size_hint_y=None, height=dp(35))
            check = Button(text="✓" if task.completed else "□", font_size=dp(17), color=GREEN if task.completed else TEXT_MUTED,
                           background_normal="", background_color=(0, 0, 0, 0), size_hint=(None, 1), width=dp(26))
            check.bind(on_release=lambda _button, task_id=task.id: self._complete_task(task_id))
            row.add_widget(check); row.add_widget(label(task.title, 11))
            if task.priority:
                row.add_widget(label(task.priority, 9, RED if task.priority == "High" else ACCENT, True))
            card.add_widget(row)
        self.content.add_widget(card)

    def _habits_card(self):
        card = Card(orientation="vertical", padding=dp(13), size_hint_y=None, height=dp(128))
        card.add_widget(label(f"HABITS  {self.state.completed_habits}/{len(self.state.habits)}", 9, TEXT_MUTED, True))
        for habit in self.state.habits[:3]:
            row = BoxLayout(size_hint_y=None, height=dp(26))
            row.add_widget(label(("✓   " if habit.completed else "□   ") + habit.name, 11))
            row.add_widget(label("🔥 " + str(habit.streak_days) + "d", 10, ACCENT, True))
            card.add_widget(row)
        self.content.add_widget(card)

    def _tasks(self):
        self._title("Tasks", "Plan, track & build habits", self._open_task_editor, "+ Add")
        self._filters(("Today⌄", "All", "Tasks", "Habits")); self._tasks_card(); self._habits_card()

    def _wealth(self):
        self._title("Wealth", "Money, loans, investments & net worth"); self._wealth_card(); self._stat_grid()

    def _goals(self):
        self._title("Goals", "Long-term targets with visible progress")
        for goal in self.state.goals:
            card = Card(orientation="vertical", padding=dp(13), size_hint_y=None, height=dp(100))
            card.add_widget(label(goal.title, 12, TEXT, True))
            card.add_widget(label(f"₹{self._money(goal.current)} / ₹{self._money(goal.target)}", 10, TEXT_MUTED))
            card.add_widget(ProgressBar(max=100, value=goal.progress_percent, size_hint_y=None, height=dp(7)))
            self.content.add_widget(card)

    def _insights(self):
        self._title("Insights", "Trends, reports & personal growth"); self._stat_grid()
        card = Card(orientation="vertical", padding=dp(13), size_hint_y=None, height=dp(135))
        card.add_widget(label("KEY TAKEAWAYS", 9, TEXT_MUTED, True))
        for text in ("Wealth grew by 4.8% this month.", "Task completion is up by 12%.", "Habit consistency is at 83%."):
            card.add_widget(label("•  " + text, 11))
        self.content.add_widget(card)

    def _stat_grid(self):
        grid = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(138))
        for title, value, color in (("ASSETS", self.state.wealth.assets, GREEN), ("LIABILITIES", self.state.wealth.liabilities, RED),
                                    ("INVESTMENTS", self.state.wealth.investments, GREEN), ("EXPENSES", self.state.wealth.monthly_expenses, ACCENT)):
            card = Card(orientation="vertical", padding=dp(11), spacing=dp(2))
            card.add_widget(label(title, 9, TEXT_MUTED, True)); card.add_widget(label(f"₹{self._money(value)}", 17, color, True)); card.add_widget(label("This month", 9, TEXT_MUTED))
            grid.add_widget(card)
        self.content.add_widget(grid)

    def _filters(self, values: tuple[str, ...]):
        row = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(4))
        for index, value in enumerate(values): row.add_widget(button(value, active=index == 0))
        self.content.add_widget(row)

    def _complete_task(self, task_id: str):
        complete_task(self.state, task_id, self.task_repository); self.show_tab(self.active_tab)

    def _open_task_editor(self, *_args):
        form = BoxLayout(orientation="vertical", padding=dp(18), spacing=dp(10))
        title_input = TextInput(hint_text="Task title", multiline=False, size_hint_y=None, height=dp(44))
        priority_input = Spinner(text="Medium", values=("High", "Medium", "Low"), size_hint_y=None, height=dp(44))
        difficulty_input = Spinner(text="Difficulty 3", values=tuple(f"Difficulty {v}" for v in range(1, 6)), size_hint_y=None, height=dp(44))
        importance_input = Spinner(text="Importance 3", values=tuple(f"Importance {v}" for v in range(1, 6)), size_hint_y=None, height=dp(44))
        for item in (label("NEW TASK", 12, GREEN, True), title_input, priority_input, difficulty_input, importance_input): form.add_widget(item)
        feedback = label("", 11, RED); form.add_widget(feedback)
        popup = Popup(title="Add task", content=form, size_hint=(.9, None), height=dp(390), separator_color=GREEN)
        actions = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8)); cancel = button("Cancel"); cancel.bind(on_release=popup.dismiss); save = button("Save task", active=True)

        def save_task(_button):
            try:
                add_task(self.state, title_input.text, priority_input.text, int(difficulty_input.text.rsplit(" ", 1)[-1]), int(importance_input.text.rsplit(" ", 1)[-1]), self.task_repository)
            except ValueError as error:
                feedback.text = str(error); return
            popup.dismiss(); self.show_tab("Tasks")

        save.bind(on_release=save_task); actions.add_widget(cancel); actions.add_widget(save); form.add_widget(actions); popup.open()

    @staticmethod
    def _money(value) -> str:
        return f"{value:,.0f}"
