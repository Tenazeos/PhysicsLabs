import numpy as np
import pytest

from labs.magnetic_trap.calculations.magnetic_field import MagneticFieldFromRing
from labs.magnetic_trap.models import SegmentedRing
from tests.magnetic_trap.theoretical import evaluate_field_at_height


@pytest.mark.parametrize("height", [1, 10, 100])
def test_magnetic_field_value(height: float, ring: SegmentedRing) -> None:
    field = MagneticFieldFromRing(ring, current=1)

    assert np.linalg.norm(field(np.array([0, 0, height]))) == pytest.approx(
        evaluate_field_at_height(ring, height), abs=1e-5, rel=1e-3
    )
