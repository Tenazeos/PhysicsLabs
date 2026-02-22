from copy import copy

import numpy as np
import pytest

from labs.the_capacitor.calculations.charge import calculate_charge
from labs.the_capacitor.model import Capacitor, Plate


@pytest.fixture(scope="session", params=[[40, 0.4], [50, 0.5], [60, 0.6]])
def capacitor(request) -> Capacitor:
    side, distance = request.param
    plate = Plate(
        length=side,
        width=side,
        chunk_side=1,
    )
    return Capacitor(upper_plate=plate, lower_plate=copy(plate), distance=distance, voltage=2.0)


@pytest.fixture(scope="session")
def charge(capacitor: Capacitor) -> np.ndarray:
    return calculate_charge(capacitor)
