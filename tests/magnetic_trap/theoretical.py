import numpy as np

from labs.magnetic_trap.models import SegmentedRing


def evaluate_field_at_height(ring: SegmentedRing, height: float, current: float = 1.0) -> float:
    height = abs(ring.z_cord - height)
    return 2 * np.pi * current * ring.radius**2 / (ring.radius**2 + height**2) ** (3 / 2)
