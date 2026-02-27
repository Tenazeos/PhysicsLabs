import numpy as np

from labs.the_capacitor.calculations.util import measure_capacity
from labs.the_capacitor.model import RectCapacitor

from ..theoretical_solution import evaluate_capacity


def test_capacity_is_close_to_theoretical(capacitor: RectCapacitor, charge: np.ndarray):
    subcapacitor, lower_charge, upper_charge = (
        capacitor,
        charge[: capacitor.lower_plate.chunk_count],
        charge[capacitor.lower_plate.chunk_count :],
    )

    qu = np.sum(upper_charge)
    ql = np.sum(lower_charge)
    assert abs(qu + ql) / max(abs(qu), abs(ql)) < 0.05, (
        "Charge distribution is not symmetric in the center (sum of +- should be close to zero)"
    )

    measured = measure_capacity(subcapacitor, np.concatenate([lower_charge, upper_charge]))
    expected = evaluate_capacity(subcapacitor)

    assert abs(measured - expected) / max(expected, measured) < 0.05, (
        f"Capacity of the central area {measured:.2f} is not close enough to the theoretical "
        f"value {expected:.2f}"
    )
