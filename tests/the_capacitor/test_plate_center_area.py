"""
Рассмотрим центральную область пластин, сторона которой в 2 раза меньше, чем у исходных пластин.
В этой области электрическое поле должно быть почти однородным, и емкость должна быть близка к
теоретической для идеального плоского конденсатора.
"""

import numpy as np

from labs.the_capacitor.calculations.strength import ElectricFieldStrength
from labs.the_capacitor.calculations.util import measure_capacity
from labs.the_capacitor.model import Capacitor
from tests.the_capacitor.util import extract_central_area

from .theoretical_solution import evaluate_capacity


def test_electric_field_is_vertical_at_center_of_plate(capacitor: Capacitor, charge: np.ndarray):
    # Введем относительную величину "вертикальности" поля, которая будет равна 0, если поле
    # полностью вертикальное, и будет расти, если поле будет отклоняться от вертикали
    # На самом деле это tg(alpha) := max(x, y) / z на компонентах векторного поля
    subcapacitor, lower_charge, upper_charge = extract_central_area(capacitor, charge)

    # Проверим вертикальность по всей высоте между обкладками
    for distance_coef in np.arange(0.1, 1, 0.1):
        center_field = ElectricFieldStrength(
            subcapacitor, np.concatenate([lower_charge, upper_charge])
        )
        grid = subcapacitor.chunks_vector[: subcapacitor.lower_plate.chunk_count] + np.array(
            [[0, 0, subcapacitor.distance * distance_coef]]
        )
        f = np.array([center_field(point) for point in grid])
        metric = np.max((f[:, 0], f[:, 1])) / f[:, 2]

        assert np.count_nonzero(metric < 0.02) / metric.shape[0] > 0.98, (
            "Electric field is not vertical enough at the center of the plate"
        )


def test_capacity_of_central_area_is_close_to_theoretical(capacitor: Capacitor, charge: np.ndarray):
    # subcapacitor, lower_charge, upper_charge = extract_central_area(capacitor, charge)
    subcapacitor, lower_charge, upper_charge = (
        capacitor,
        charge[: capacitor.lower_plate.chunk_count],
        charge[capacitor.lower_plate.chunk_count :],
    )

    qu = np.sum(upper_charge)
    ql = np.sum(lower_charge)
    assert abs(qu + ql) / max(abs(qu), abs(ql)) < 0.1, (
        "Charge distribution is not symmetric in the center (sum of +- should be close to zero)"
    )

    measured = measure_capacity(subcapacitor, np.concatenate([lower_charge, upper_charge]))
    expected = evaluate_capacity(subcapacitor)

    assert abs(measured - expected) / max(expected, measured) < 0.05, (
        f"Capacity of the central area {measured:.2f} is not close enough to the theoretical "
        f"value {expected:.2f}"
    )
