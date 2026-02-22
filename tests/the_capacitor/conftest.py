from copy import copy

import pytest

from labs.the_capacitor.model import Capacitor, Plate


@pytest.fixture
def square_capacitor() -> Capacitor:
    plate = Plate(
        length=30,
        width=30,
        chunk_side=1,
    )
    return Capacitor(
        lower_plate=plate,
        upper_plate=copy(plate),
        distance=30,
        voltage=100,
    )
