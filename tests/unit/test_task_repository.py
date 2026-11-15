from app.core.app_state import create_demo_state
from app.data.repositories.task_repository import InMemoryTaskRepository


def test_in_memory_repository_returns_copies() -> None:
    repository = InMemoryTaskRepository(create_demo_state().tasks)
    tasks = repository.list_tasks()
    tasks[0].title = "Changed locally"

    assert repository.list_tasks()[0].title != "Changed locally"


def test_in_memory_repository_saves_task() -> None:
    state = create_demo_state()
    repository = InMemoryTaskRepository()

    repository.save(state.tasks[0])

    assert repository.list_tasks()[0].id == "task-1"
