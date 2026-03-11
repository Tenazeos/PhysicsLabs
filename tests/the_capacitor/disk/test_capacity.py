import numpy as np

from labs.the_capacitor.calculations.util import measure_capacity
from labs.the_capacitor.model import DiskCapacitor

from ..theoretical_solution import evaluate_capacity
from .util import extract_central_disk


def test_central_area_capacity_is_close_to_theoretical(
    capacitor: DiskCapacitor, charge: np.ndarray
):
    subcapacitor, lower_charge, upper_charge = extract_central_disk(capacitor, charge)

    qu = np.sum(upper_charge)
    ql = np.sum(lower_charge)
    assert abs(qu + ql) / max(abs(qu), abs(ql)) < 0.01, (
        "Charge distribution is not symmetric (sum of +- should be close to zero)"
    )

    measured = measure_capacity(subcapacitor, np.concatenate([lower_charge, upper_charge]))
    expected = evaluate_capacity(subcapacitor)

    assert abs(measured - expected) / max(expected, measured) < 0.1, (
        f"Capacity of the central area {measured:.2f} is not close to the theoretical "
        f"value {expected:.2f} for capacitor with distance {subcapacitor.distance} between plates"
    )
