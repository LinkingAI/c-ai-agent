import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from inflation_calculator import YearlyProjection, calculate_inaction_cost


def test_calculate_inaction_cost_basic():
    projections = calculate_inaction_cost(1000, 0.05, 2)
    assert len(projections) == 2
    assert math.isclose(projections[0].real_value, 952.38095, rel_tol=1e-6)
    assert math.isclose(projections[0].loss, 47.61905, rel_tol=1e-6)
    assert isinstance(projections[0], YearlyProjection)
    assert projections[1].year == 2
    assert projections[1].loss > projections[0].loss


def test_calculate_inaction_cost_invalid_inputs():
    with pytest.raises(ValueError):
        calculate_inaction_cost(0, 0.05, 1)
    with pytest.raises(ValueError):
        calculate_inaction_cost(1000, -0.01, 1)
    with pytest.raises(ValueError):
        calculate_inaction_cost(1000, 0.05, 0)
