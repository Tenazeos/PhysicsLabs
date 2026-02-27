from copy import copy

import numpy as np
import pytest

from labs.the_capacitor.calculations.charge import calculate_charge
from labs.the_capacitor.model import RectCapacitor, RectPlate


@pytest.fixture(scope="session", params=[[50, 0.5], [50, 5], [50, 25]])
def capacitor(request) -> RectCapacitor:
    side, distance = request.param
    plate = RectPlate(
        length=side,
        width=side,
        chunk_side=1,
    )
    return RectCapacitor(upper_plate=plate, lower_plate=copy(plate), distance=distance, voltage=2.0)


@pytest.fixture(scope="session")
def charge(capacitor: RectCapacitor) -> np.ndarray:
    return calculate_charge(capacitor)
