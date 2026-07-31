from copy import copy

import numpy as np
import pytest

from labs.the_capacitor.calculations.charge import calculate_charge
from labs.the_capacitor.model import DiskCapacitor, DiskPlate


@pytest.fixture(
    scope="session",
    params=[(5, 1, 0.125), (5, 1.5, 0.125), (5, 2, 0.125), (40, 5, 1), (40, 10, 1)],
)
def capacitor(request) -> DiskCapacitor:
    """
    При моделировании конденсатора нужно соблюдать несколько соотношений:
    1. Радиус конденсатора должен быть значительно больше расстояния между пластинами
    2. Расстояние между пластинами должно быть достаточно большим, чтобы избежать сильного влияния
      дискретизации (то что мы считаем заряды – точечными)
    3. При этом, чтобы тесты считались за разумное время, мы придерживаемся радиуса около 40 точек
    """
    radius, distance, dr = request.param
    plate = DiskPlate(radius=radius, dr=dr)
    return DiskCapacitor(upper_plate=plate, lower_plate=copy(plate), distance=distance, voltage=2.0)


@pytest.fixture(scope="session")
def charge(capacitor: DiskCapacitor) -> np.ndarray:
    return calculate_charge(capacitor)
