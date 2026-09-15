"""Core ROI (Return on Investment) calculation engine.

This module implements the business logic for calculating the economic
value of a project or resource allocation, given the hours spent, the
hourly rate of the resource, and the expected financial benefit.

It is intentionally kept free of any UI, database, API, or integration
concerns (Jira, GitHub, Streamlit, etc.). It exposes a single pure
function, ``calculate_roi``, that performs input validation and the
ROI calculation and returns the result as a dictionary.
"""

from numbers import Real


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


def calculate_roi(hours: float, hourly_rate: float, benefit: float) -> dict:
    """Calculate the total cost, net benefit, and ROI percentage.

    Args:
        hours: Number of hours spent by a resource. Must be a
            non-negative, non-boolean number.
        hourly_rate: Cost/rate per working hour. Must be a
            non-negative, non-boolean number.
        benefit: Expected financial benefit or savings. May be
            positive, zero, or negative (a negative value represents
            an expected financial loss). Must be a non-boolean number.

    Returns:
        A dictionary with the following keys:
            - "hours": the validated input hours.
            - "hourly_rate": the validated input hourly rate.
            - "benefit": the validated input benefit.
            - "total_cost": ``hours * hourly_rate``.
            - "net_benefit": ``benefit - total_cost``.
            - "roi_percentage": ``(net_benefit / total_cost) * 100``,
              or ``0.0`` when ``total_cost`` is zero (see below).

    Raises:
        ValueError: If ``hours`` or ``hourly_rate`` is negative or
            non-numeric, or if ``benefit`` is non-numeric. Boolean
            values are explicitly rejected for all three parameters,
            since ``bool`` is a subclass of ``int`` in Python.

    Formulas:
        total_cost = hours * hourly_rate
        net_benefit = benefit - total_cost
        roi_percentage = (net_benefit / total_cost) * 100

    Zero-cost behavior:
        ROI is mathematically undefined when ``total_cost`` is zero
        (division by zero). As an explicit MVP business rule, this
        function does not raise ``ZeroDivisionError`` in that case;
        instead it returns ``roi_percentage = 0.0`` while still
        computing ``total_cost`` and ``net_benefit`` correctly.
    """
    _validate_non_negative_numeric(hours, "hours")
    _validate_non_negative_numeric(hourly_rate, "hourly_rate")
    _validate_numeric(benefit, "benefit")

    total_cost = hours * hourly_rate
    net_benefit = benefit - total_cost

    if total_cost == 0:
        roi_percentage = 0.0
    else:
        roi_percentage = (net_benefit / total_cost) * 100

    return {
        "hours": hours,
        "hourly_rate": hourly_rate,
        "benefit": benefit,
        "total_cost": total_cost,
        "net_benefit": net_benefit,
        "roi_percentage": roi_percentage,
    }
