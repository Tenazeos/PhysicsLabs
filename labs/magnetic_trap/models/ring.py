from dataclasses import dataclass
from functools import cached_property

import numpy as np


@dataclass(slots=True)
class SegmentedRing:
    segment_count: int
    radius: float
    z_cord: float

    @cached_property
    def points(self) -> np.ndarray:
        phi = np.linspace(0, 2 * np.pi, num=self.segment_count, endpoint=False)
        x = self.radius * np.cos(phi)
        y = self.radius * np.sin(phi)
        z = np.ones(self.segment_count) * self.z_cord

        return np.stack([x, y, z], axis=1)

    @cached_property
    def dl(self) -> np.ndarray:
        return np.diff(self.points, axis=0, append=self.points[0:1])


@dataclass(slots=True)
class MagneticTrap:
    upper_ring: SegmentedRing
    lower_ring: SegmentedRing
    current_strength: float
