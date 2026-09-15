"""Unit tests for the TaskCollection container (src/task_collection.py).

These tests verify that ``TaskCollection`` can store multiple ``Task``
objects, return them all, report how many are stored, and reject
anything that is not a valid ``Task`` instance. No ROI calculations
are exercised here.
"""

import pytest

from task import Task
from task_collection import TaskCollection


def _make_task(name: str = "Task", hours: float = 10, hourly_rate: float = 100, expected_benefit: float = 500) -> Task:
    return Task(name=name, hours=hours, hourly_rate=hourly_rate, expected_benefit=expected_benefit)


# ---------------------------------------------------------------------------
# Empty collection
# ---------------------------------------------------------------------------


def test_new_collection_is_empty():
    collection = TaskCollection()

    assert collection.get_all_tasks() == []
    assert collection.count() == 0


# ---------------------------------------------------------------------------
# Adding a single task
# ---------------------------------------------------------------------------


def test_add_single_task_stores_it():
    collection = TaskCollection()
    task = _make_task(name="Automate report")

    collection.add_task(task)

    assert collection.count() == 1
    assert collection.get_all_tasks() == [task]


# ---------------------------------------------------------------------------
# Adding multiple tasks does not replace existing tasks
# ---------------------------------------------------------------------------


def test_add_multiple_tasks_keeps_all_of_them():
    collection = TaskCollection()
    task_one = _make_task(name="Task One")
    task_two = _make_task(name="Task Two")
    task_three = _make_task(name="Task Three")

    collection.add_task(task_one)
    collection.add_task(task_two)
    collection.add_task(task_three)

    assert collection.count() == 3
    assert collection.get_all_tasks() == [task_one, task_two, task_three]


def test_add_task_preserves_insertion_order():
    collection = TaskCollection()
    task_a = _make_task(name="A")
    task_b = _make_task(name="B")

    collection.add_task(task_a)
    collection.add_task(task_b)

    assert collection.get_all_tasks() == [task_a, task_b]


# ---------------------------------------------------------------------------
# get_all_tasks returns a copy
# ---------------------------------------------------------------------------


def test_get_all_tasks_returns_a_copy_not_internal_reference():
    collection = TaskCollection()
    collection.add_task(_make_task())

    returned = collection.get_all_tasks()
    returned.append(_make_task(name="Injected"))

    assert collection.count() == 1


# ---------------------------------------------------------------------------
# count()
# ---------------------------------------------------------------------------


def test_count_matches_number_of_added_tasks():
    collection = TaskCollection()

    for i in range(5):
        collection.add_task(_make_task(name=f"Task {i}"))

    assert collection.count() == 5


# ---------------------------------------------------------------------------
# Only valid Task objects can be added
# ---------------------------------------------------------------------------


def test_add_task_rejects_non_task_string():
    collection = TaskCollection()

    with pytest.raises(TypeError):
        collection.add_task("not a task")


def test_add_task_rejects_non_task_dict():
    collection = TaskCollection()

    with pytest.raises(TypeError):
        collection.add_task({"name": "Task", "hours": 10, "hourly_rate": 100, "expected_benefit": 500})


def test_add_task_rejects_none():
    collection = TaskCollection()

    with pytest.raises(TypeError):
        collection.add_task(None)


def test_add_task_rejects_invalid_object_without_mutating_collection():
    collection = TaskCollection()
    collection.add_task(_make_task())

    with pytest.raises(TypeError):
        collection.add_task(123)

    assert collection.count() == 1
