from __future__ import annotations

from functools import cached_property
from typing import Protocol

import numpy as np


class Capacitor(Protocol):
    lower_plate: Plate
    upper_plate: Plate
    distance: float
    voltage: float

    @cached_property
    def chunks_vector(self) -> np.ndarray: ...


class Plate(Protocol):
    @property
    def chunk_count(self) -> int: ...

    @property
    def area(self) -> float: ...
