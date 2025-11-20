import pytest
from datetime import datetime
import time
import argparse

from src.app_code import User, Task
user: User | None = None

def setup_module(module):
    global user
    args = argparse.Namespace(
        hostname="riku.shoshin.uwaterloo.ca", database="SE101_Team_27", username="a88mehta", password="251016")
    user = User(representative_username=args.username, representative_password=args.password, database=args.database, hostname=args.hostname)


def teardown_module(module):
    global user
    if user:
        # best-effort cleanup: don't raise on errors
        try:
            # remove test leftovers if any
            tasks = user.fetch_tasks()
            for t in tasks:
                if t.item().startswith("Test") or t.item().startswith("Next") or t.item().startswith("Nonexistent"):
                    user.delete_task(t.item())
        except Exception:
            pass

def delete_task(item_name: str):
    global user
    user.delete_task(item_name)

@pytest.mark.smoke
@pytest.mark.regression
def test_add_success():
    global user
    unique_name = f"Test Task {int(time.time())}"
    task = Task(item=unique_name, type="Work", started=datetime(2025, 10, 1, 9, 0, 0), due=datetime(2025, 10, 2, 17, 0, 0), done=None)
    delete_task(unique_name)
    assert all(t.item() != unique_name for t in user.fetch_tasks())
    assert user.add_task(task) is True
    tasks = user.fetch_tasks()
    assert any(t.item() == unique_name for t in tasks)
    user.print_tasks()
    delete_task(unique_name)


@pytest.mark.regression
def test_add_duplicate():
    global user
    unique_name = f"Test Task {int(time.time())}_dup"
    task = Task(item=unique_name, type="Work", started=datetime(2025, 10, 1, 9, 0, 0), due=datetime(2025, 10, 2, 17, 0, 0), done=None)
    delete_task(unique_name)
    assert all(t.item() != unique_name for t in user.fetch_tasks())
    assert user.add_task(task) is True
    # Try to add again (should fail)
    assert user.add_task(task) is False
    tasks = [t for t in user.fetch_tasks() if t.item() == unique_name]
    assert len(tasks) == 1
    user.print_tasks()
    delete_task(unique_name)

@pytest.mark.regression
def test_update_success():
    global user
    unique_name = f"Test Task Update {int(time.time())}"
    original_task = Task(item=unique_name, type="Work", started=datetime(2025, 10, 1, 9, 0, 0), due=datetime(2025, 10, 2, 17, 0, 0), done=None)
    updated_task = Task(item=unique_name, type="Personal", started=datetime(2025, 10, 3, 10, 0, 0), due=datetime(2025, 10, 4, 18, 0, 0), done=datetime(2025, 10, 5, 12, 0, 0))
    delete_task(unique_name)
    assert user.add_task(original_task) is True
    assert user.update_task(updated_task) is True
    tasks = [t for t in user.fetch_tasks() if t.item() == unique_name]
    assert len(tasks) == 1
    t = tasks[0]
    assert t.type() == "Personal"
    assert t.started() == datetime(2025, 10, 3, 10, 0, 0)
    assert t.due() == datetime(2025, 10, 4, 18, 0, 0)
    assert t.done() == datetime(2025, 10, 5, 12, 0, 0)
    user.print_tasks()
    delete_task(unique_name)


@pytest.mark.regression
def test_update_nonexistent():
    global user
    unique_name = f"Nonexistent Task {int(time.time())}"
    updated_task = Task(item=unique_name, type="Errand", started=datetime(2025, 10, 6, 8, 0, 0), due=datetime(2025, 10, 7, 17, 0, 0), done=None)
    delete_task(unique_name)
    assert user.update_task(updated_task) is False
    assert all(t.item() != unique_name for t in user.fetch_tasks())

@pytest.mark.smoke
def delete_task(item_name: str):
    global user
    user.delete_task(item_name)

@pytest.mark.regression
def test_next_no_tasks():
    global user
    tasks = user.fetch_tasks()
    for t in tasks:
        user.delete_task(t.item())
    assert user.next_task() is None


@pytest.mark.smoke
@pytest.mark.regression
def test_next_single_task():
    global user
    unique_name = f"Next Single {int(time.time())}"
    task = Task(item=unique_name, type="Work", started=datetime(2025, 10, 10, 9, 0, 0), due=datetime(2025, 10, 11, 17, 0, 0), done=None)
    delete_task(unique_name)
    user.add_task(task)
    result = user.next_task()
    assert result is not None
    assert result.item() == unique_name
    delete_task(unique_name)


@pytest.mark.regression
def test_next_multiple_tasks():
    global user
    names = [f"Next Multi {i} {int(time.time())}" for i in range(3)]
    for n in names:
        delete_task(n)
    tasks = [
        Task(item=names[0], type="Work", started=datetime(2025, 10, 10, 9, 0, 0), due=datetime(2025, 10, 12, 17, 0, 0), done=None),
        Task(item=names[1], type="Work", started=datetime(2025, 10, 10, 9, 0, 0), due=datetime(2025, 10, 11, 17, 0, 0), done=None),
        Task(item=names[2], type="Work", started=datetime(2025, 10, 10, 9, 0, 0), due=datetime(2025, 10, 13, 17, 0, 0), done=None),
    ]
    for t in tasks:
        user.add_task(t)
    result = user.next_task()
    assert result is not None
    assert result.item() == names[1]
    for n in names:
        delete_task(n)
        
@pytest.mark.regression
def test_today_task():
    """A task due today should be returned by next_task() over a task due tomorrow."""
    global user
    now = datetime.now()
    today = now
    tomorrow = now + timedelta(days=1)
    name_today = f"Today Task {int(time.time())}"
    name_tomorrow = f"Tomorrow Task {int(time.time())}"
    task_today = Task(item=name_today, type="Work", started=today.replace(hour=9, minute=0, second=0, microsecond=0), due=today.replace(hour=17, minute=0, second=0, microsecond=0), done=None)
    task_tomorrow = Task(item=name_tomorrow, type="Work", started=today.replace(hour=9, minute=0, second=0, microsecond=0), due=tomorrow.replace(hour=17, minute=0, second=0, microsecond=0), done=None)
    delete_task(name_today)
    delete_task(name_tomorrow)
    
    # ensure no other tasks exist that could interfere
    tasks = user.fetch_tasks()
    for t in tasks:
        user.delete_task(t.item())
        
    user.add_task(task_tomorrow)
    user.add_task(task_today)
    result = user.next_task()
    assert result is not None
    assert result.item() == name_today
    delete_task(name_today)
    delete_task(name_tomorrow)


