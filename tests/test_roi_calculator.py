"""Unit tests for the ROI calculation engine (src/roi_calculator.py).

These tests verify observable behavior of ``calculate_roi``: the
returned values for normal, zero-cost, boundary, and numerical cases,
and the ``ValueError`` raised for invalid inputs.
"""

import pytest

from roi_calculator import calculate_roi


# ---------------------------------------------------------------------------
# Normal cases
# ---------------------------------------------------------------------------


def test_calculate_roi_standard_profitable_case():
    result = calculate_roi(10, 100, 2000)

    assert result["total_cost"] == pytest.approx(1000)
    assert result["net_benefit"] == pytest.approx(1000)
    assert result["roi_percentage"] == pytest.approx(100.0)


def test_calculate_roi_zero_benefit():
    result = calculate_roi(10, 100, 0)

    assert result["total_cost"] == pytest.approx(1000)
    assert result["net_benefit"] == pytest.approx(-1000)
    assert result["roi_percentage"] == pytest.approx(-100.0)


def test_calculate_roi_benefit_equal_to_total_cost():
    result = calculate_roi(10, 100, 1000)

    assert result["total_cost"] == pytest.approx(1000)
    assert result["net_benefit"] == pytest.approx(0)
    assert result["roi_percentage"] == pytest.approx(0.0)


def test_calculate_roi_high_roi_scenario():
    result = calculate_roi(1, 10, 10_000)

    assert result["total_cost"] == pytest.approx(10)
    assert result["net_benefit"] == pytest.approx(9990)
    assert result["roi_percentage"] == pytest.approx(99_900.0)


def test_calculate_roi_negative_net_benefit_loss_scenario():
    result = calculate_roi(10, 100, 500)

    assert result["total_cost"] == pytest.approx(1000)
    assert result["net_benefit"] == pytest.approx(-500)
    assert result["roi_percentage"] == pytest.approx(-50.0)


# ---------------------------------------------------------------------------
# Zero-cost cases
# ---------------------------------------------------------------------------


def test_calculate_roi_zero_hours():
    result = calculate_roi(0, 100, 500)

    assert result["total_cost"] == 0
    assert result["net_benefit"] == pytest.approx(500)
    assert result["roi_percentage"] == 0.0


def test_calculate_roi_zero_hourly_rate():
    result = calculate_roi(10, 0, 500)

    assert result["total_cost"] == 0
    assert result["net_benefit"] == pytest.approx(500)
    assert result["roi_percentage"] == 0.0


def test_calculate_roi_zero_hours_and_zero_hourly_rate():
    result = calculate_roi(0, 0, 500)

    assert result["total_cost"] == 0
    assert result["net_benefit"] == pytest.approx(500)
    assert result["roi_percentage"] == 0.0


# ---------------------------------------------------------------------------
# Validation cases
# ---------------------------------------------------------------------------


def test_calculate_roi_negative_hours_raises_value_error():
    with pytest.raises(ValueError):
        calculate_roi(-5, 100, 1000)


def test_calculate_roi_negative_hourly_rate_raises_value_error():
    with pytest.raises(ValueError):
        calculate_roi(5, -100, 1000)


@pytest.mark.parametrize(
    ("hours", "hourly_rate", "benefit"),
    [
        pytest.param("five", 100, 1000, id="string_hours"),
        pytest.param(5, "100", 1000, id="string_hourly_rate"),
        pytest.param(5, 100, "1000", id="string_benefit"),
        pytest.param(True, 100, 1000, id="boolean_hours"),
        pytest.param(5, True, 1000, id="boolean_hourly_rate"),
        pytest.param(5, 100, True, id="boolean_benefit"),
    ],
)
def test_calculate_roi_invalid_inputs_raise_value_error(hours, hourly_rate, benefit):
    with pytest.raises(ValueError):
        calculate_roi(hours, hourly_rate, benefit)


# ---------------------------------------------------------------------------
# Boundary / numerical cases
# ---------------------------------------------------------------------------


def test_calculate_roi_very_small_positive_values():
    result = calculate_roi(0.001, 0.001, 0.001)

    expected_total_cost = 0.001 * 0.001
    expected_net_benefit = 0.001 - expected_total_cost
    expected_roi = (expected_net_benefit / expected_total_cost) * 100

    assert result["total_cost"] == pytest.approx(expected_total_cost)
    assert result["net_benefit"] == pytest.approx(expected_net_benefit)
    assert result["roi_percentage"] == pytest.approx(expected_roi)


def test_calculate_roi_large_numeric_values():
    hours = 1_000_000
    hourly_rate = 500
    benefit = 1_000_000_000

    result = calculate_roi(hours, hourly_rate, benefit)

    expected_total_cost = hours * hourly_rate
    expected_net_benefit = benefit - expected_total_cost
    expected_roi = (expected_net_benefit / expected_total_cost) * 100

    assert result["total_cost"] == pytest.approx(expected_total_cost)
    assert result["net_benefit"] == pytest.approx(expected_net_benefit)
    assert result["roi_percentage"] == pytest.approx(expected_roi)


def test_calculate_roi_floating_point_inputs():
    result = calculate_roi(7.5, 42.25, 950.75)

    expected_total_cost = 7.5 * 42.25
    expected_net_benefit = 950.75 - expected_total_cost
    expected_roi = (expected_net_benefit / expected_total_cost) * 100

    assert result["total_cost"] == pytest.approx(expected_total_cost)
    assert result["net_benefit"] == pytest.approx(expected_net_benefit)
    assert result["roi_percentage"] == pytest.approx(expected_roi)


# ---------------------------------------------------------------------------
# Return shape / purity
# ---------------------------------------------------------------------------


def test_calculate_roi_returns_all_expected_keys():
    result = calculate_roi(10, 100, 2000)

    assert set(result.keys()) == {
        "hours",
        "hourly_rate",
        "benefit",
        "total_cost",
        "net_benefit",
        "roi_percentage",
    }


def test_calculate_roi_is_deterministic_pure_function():
    first_call = calculate_roi(10, 100, 2000)
    second_call = calculate_roi(10, 100, 2000)

    assert first_call == second_call
