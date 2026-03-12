from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

import numpy as np

from .util.disk import (
    count_disk_plate_charges,
    generate_disk_capacitor_chunks_vector,
    generate_disk_plate_vector,
)


@dataclass
class DiskCapacitor:
    lower_plate: DiskPlate
    upper_plate: DiskPlate
    distance: float
    voltage: float

    @property
    def dr(self) -> float:
        return self.lower_plate.dr

    @cached_property
    def chunks_vector(self) -> np.ndarray:
        return generate_disk_capacitor_chunks_vector(self)

    @cached_property
    def covering_chunks_at_zero_height(self) -> np.ndarray:
        excess_radius_coef = 0.2  # +20%

        max_radius = max(self.lower_plate.radius, self.upper_plate.radius)
        excess_radius = round(excess_radius_coef * max_radius / self.dr) * self.dr

        return generate_disk_plate_vector(
            radius=max_radius + excess_radius,
            dr=self.dr,
            z_coord=0,
        )


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
