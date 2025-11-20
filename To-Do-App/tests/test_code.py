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

