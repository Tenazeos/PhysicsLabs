from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

import numpy as np

from .util.disk import (
    count_disk_plate_charges,
    generate_disk_capacitor_chunks_vector,
)


@dataclass
class DiskCapacitor:
    lower_plate: DiskPlate
    upper_plate: DiskPlate
    distance: float
    voltage: float

    @cached_property
    def chunks_vector(self) -> np.ndarray:
        return generate_disk_capacitor_chunks_vector(self)


@dataclass
class DiskPlate:
    radius: float
    dr: float

    @cached_property
    def chunk_count(self) -> int:
        return count_disk_plate_charges(self)

    @property
    def area(self) -> float:
        return np.pi * self.radius**2
