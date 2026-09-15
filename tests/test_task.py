"""Unit tests for the Task data model (src/task.py).

These tests verify that ``Task`` correctly stores valid data and
raises ``ValueError`` with a clear message for invalid data. ``Task``
performs no ROI calculations, so none are tested here.
"""

import pytest

from task import Task


# ---------------------------------------------------------------------------
# Valid creation / storage
# ---------------------------------------------------------------------------


def test_task_valid_creation_stores_all_fields():
    task = Task(
        name="Automate monthly report",
        hours=20,
        hourly_rate=120,
        expected_benefit=5000,
    )

    assert task.name == "Automate monthly report"
    assert task.hours == 20
    assert task.hourly_rate == 120
    assert task.expected_benefit == 5000


def test_task_normal_positive_values():
    task = Task(name="Improve process", hours=8.5, hourly_rate=75.0, expected_benefit=1200.0)

    assert task.hours == pytest.approx(8.5)
    assert task.hourly_rate == pytest.approx(75.0)
    assert task.expected_benefit == pytest.approx(1200.0)


# ---------------------------------------------------------------------------
# Zero boundary values
# ---------------------------------------------------------------------------


def test_task_zero_hours_is_valid():
    task = Task(name="Quick task", hours=0, hourly_rate=100, expected_benefit=500)

    assert task.hours == 0


def test_task_zero_hourly_rate_is_valid():
    task = Task(name="Volunteer task", hours=10, hourly_rate=0, expected_benefit=500)

    assert task.hourly_rate == 0


def test_task_zero_expected_benefit_is_valid():
    task = Task(name="Break-even task", hours=10, hourly_rate=100, expected_benefit=0)

    assert task.expected_benefit == 0


def test_task_zero_hours_and_hourly_rate_is_valid():
    task = Task(name="No cost task", hours=0, hourly_rate=0, expected_benefit=500)

    assert task.hours == 0
    assert task.hourly_rate == 0


# ---------------------------------------------------------------------------
# Negative expected benefit is explicitly allowed
# ---------------------------------------------------------------------------


def test_task_negative_expected_benefit_is_valid():
    task = Task(name="Loss-making task", hours=10, hourly_rate=100, expected_benefit=-500)

    assert task.expected_benefit == -500


# ---------------------------------------------------------------------------
# Invalid name
# ---------------------------------------------------------------------------


def test_task_empty_name_raises_value_error():
    with pytest.raises(ValueError):
        Task(name="", hours=10, hourly_rate=100, expected_benefit=500)


def test_task_whitespace_only_name_raises_value_error():
    with pytest.raises(ValueError):
        Task(name="   ", hours=10, hourly_rate=100, expected_benefit=500)


def test_task_non_string_name_raises_value_error():
    with pytest.raises(ValueError):
        Task(name=123, hours=10, hourly_rate=100, expected_benefit=500)


# ---------------------------------------------------------------------------
# Invalid hours
# ---------------------------------------------------------------------------


def test_task_negative_hours_raises_value_error():
    with pytest.raises(ValueError):
        Task(name="Task", hours=-5, hourly_rate=100, expected_benefit=500)


def test_task_non_numeric_hours_raises_value_error():
    with pytest.raises(ValueError):
        Task(name="Task", hours="ten", hourly_rate=100, expected_benefit=500)


def test_task_boolean_hours_raises_value_error():
    with pytest.raises(ValueError):
        Task(name="Task", hours=True, hourly_rate=100, expected_benefit=500)


# ---------------------------------------------------------------------------
# Invalid hourly rate
# ---------------------------------------------------------------------------


def test_task_negative_hourly_rate_raises_value_error():
    with pytest.raises(ValueError):
        Task(name="Task", hours=10, hourly_rate=-100, expected_benefit=500)


def test_task_non_numeric_hourly_rate_raises_value_error():
    with pytest.raises(ValueError):
        Task(name="Task", hours=10, hourly_rate="high", expected_benefit=500)


def test_task_boolean_hourly_rate_raises_value_error():
    with pytest.raises(ValueError):
        Task(name="Task", hours=10, hourly_rate=False, expected_benefit=500)


# ---------------------------------------------------------------------------
# Invalid expected benefit
# ---------------------------------------------------------------------------


def test_task_non_numeric_expected_benefit_raises_value_error():
    with pytest.raises(ValueError):
        Task(name="Task", hours=10, hourly_rate=100, expected_benefit="lots")


def test_task_boolean_expected_benefit_raises_value_error():
    with pytest.raises(ValueError):
        Task(name="Task", hours=10, hourly_rate=100, expected_benefit=True)


# ---------------------------------------------------------------------------
# Task does not perform ROI calculations
# ---------------------------------------------------------------------------


def test_task_has_no_roi_calculation_attributes():
    task = Task(name="Task", hours=10, hourly_rate=100, expected_benefit=500)

    assert not hasattr(task, "total_cost")
    assert not hasattr(task, "net_benefit")
    assert not hasattr(task, "roi_percentage")
