"""Task data model.

This module defines the ``Task`` entity: a simple, validated container
for the raw data a project manager provides about a task (its name,
estimated hours, hourly rate, and expected financial benefit).

``Task`` intentionally performs no ROI or financial calculations. Its
single responsibility is to represent and validate task data. ROI,
net benefit, and cost calculations are handled separately by
``roi_calculator.calculate_roi``.
"""

from dataclasses import dataclass
from numbers import Real


def _validate_name(name: str) -> None:
    """Validate that ``name`` is a non-empty, non-whitespace-only string.

    Args:
        name: The task name to validate.

    Raises:
        ValueError: If ``name`` is not a string, or is empty or
            contains only whitespace.
    """
    if not isinstance(name, str):
        raise ValueError(f"name must be a string, got {name!r}.")
    if not name.strip():
        raise ValueError("name must not be empty or whitespace-only.")


def _validate_non_negative_numeric(value: float, field_name: str) -> None:
    """Validate that ``value`` is a non-boolean, non-negative real number.

    Args:
        value: The value to validate.
        field_name: The name of the field, used in the error message.

    Raises:
        ValueError: If ``value`` is a boolean, is not numeric, or is
            negative.
    """
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{field_name} must be numeric, got {value!r}.")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0, got {value!r}.")


def _validate_numeric(value: float, field_name: str) -> None:
    """Validate that ``value`` is a non-boolean real number.

    Args:
        value: The value to validate.
        field_name: The name of the field, used in the error message.

    Raises:
        ValueError: If ``value`` is a boolean or is not numeric.
    """
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{field_name} must be numeric, got {value!r}.")


@dataclass(frozen=True)
class Task:
    """A project task's raw estimation data.

    ``Task`` only stores and validates data. It does not calculate
    cost, net benefit, or ROI; see ``roi_calculator.calculate_roi``
    for that.

    Attributes:
        name: The task's name. Must be a non-empty, non-whitespace
            string.
        hours: Estimated hours required for the task. Must be a
            non-negative, non-boolean number.
        hourly_rate: Cost per hour of effort. Must be a non-negative,
            non-boolean number.
        expected_benefit: Expected financial benefit of the task. May
            be positive, zero, or negative. Must be a non-boolean
            number.

    Raises:
        ValueError: If any field fails validation.
    """

    name: str
    hours: float
    hourly_rate: float
    expected_benefit: float

    def __post_init__(self) -> None:
        _validate_name(self.name)
        _validate_non_negative_numeric(self.hours, "hours")
        _validate_non_negative_numeric(self.hourly_rate, "hourly_rate")
        _validate_numeric(self.expected_benefit, "expected_benefit")
