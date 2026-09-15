"""Unit tests for ROI reporting over a task collection (src/task_roi_report.py).

These tests verify that ROI can be calculated for every task in a
``TaskCollection`` (SCRUM-7), that the existing ``calculate_roi``
logic (SCRUM-4) is reused correctly, that results include both the
task and its computed ROI, and that an empty collection is handled
correctly. No sorting or prioritization is exercised here.
"""

import pytest

from roi_calculator import calculate_roi
from task import Task
from task_collection import TaskCollection
from task_roi_report import calculate_roi_for_collection, calculate_roi_for_task


def _make_task(name: str = "Task", hours: float = 10, hourly_rate: float = 100, expected_benefit: float = 500) -> Task:
    return Task(name=name, hours=hours, hourly_rate=hourly_rate, expected_benefit=expected_benefit)


# ---------------------------------------------------------------------------
# calculate_roi_for_task
# ---------------------------------------------------------------------------


def test_calculate_roi_for_task_returns_task_and_roi():
    task = _make_task(name="Automate report", hours=10, hourly_rate=100, expected_benefit=2000)

    result = calculate_roi_for_task(task)

    assert result["task"] == task
    assert result["roi"] == calculate_roi(10, 100, 2000)


def test_calculate_roi_for_task_matches_direct_calculate_roi_call():
    task = _make_task(hours=7.5, hourly_rate=42.25, expected_benefit=950.75)

    result = calculate_roi_for_task(task)

    expected = calculate_roi(task.hours, task.hourly_rate, task.expected_benefit)
    assert result["roi"] == expected


# ---------------------------------------------------------------------------
# calculate_roi_for_collection: empty collection
# ---------------------------------------------------------------------------


def test_calculate_roi_for_collection_empty_returns_empty_list():
    collection = TaskCollection()

    results = calculate_roi_for_collection(collection)

    assert results == []


# ---------------------------------------------------------------------------
# calculate_roi_for_collection: single task
# ---------------------------------------------------------------------------


def test_calculate_roi_for_collection_single_task():
    collection = TaskCollection()
    task = _make_task(name="Solo task", hours=10, hourly_rate=100, expected_benefit=1000)
    collection.add_task(task)

    results = calculate_roi_for_collection(collection)

    assert len(results) == 1
    assert results[0]["task"] == task
    assert results[0]["roi"] == calculate_roi(10, 100, 1000)


# ---------------------------------------------------------------------------
# calculate_roi_for_collection: multiple tasks
# ---------------------------------------------------------------------------


def test_calculate_roi_for_collection_multiple_tasks_returns_all_in_order():
    collection = TaskCollection()
    task_one = _make_task(name="Task One", hours=10, hourly_rate=100, expected_benefit=2000)
    task_two = _make_task(name="Task Two", hours=5, hourly_rate=50, expected_benefit=0)
    task_three = _make_task(name="Task Three", hours=0, hourly_rate=0, expected_benefit=500)

    collection.add_task(task_one)
    collection.add_task(task_two)
    collection.add_task(task_three)

    results = calculate_roi_for_collection(collection)

    assert len(results) == 3
    assert [r["task"] for r in results] == [task_one, task_two, task_three]
    assert results[0]["roi"] == calculate_roi(10, 100, 2000)
    assert results[1]["roi"] == calculate_roi(5, 50, 0)
    assert results[2]["roi"] == calculate_roi(0, 0, 500)


def test_calculate_roi_for_collection_includes_negative_roi_tasks():
    collection = TaskCollection()
    losing_task = _make_task(name="Losing task", hours=10, hourly_rate=100, expected_benefit=500)
    collection.add_task(losing_task)

    results = calculate_roi_for_collection(collection)

    assert results[0]["roi"]["roi_percentage"] == pytest.approx(-50.0)


def test_calculate_roi_for_collection_does_not_mutate_collection():
    collection = TaskCollection()
    collection.add_task(_make_task())

    calculate_roi_for_collection(collection)

    assert collection.count() == 1
