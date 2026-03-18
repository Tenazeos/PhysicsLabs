import numpy as np

from ..models import SegmentedRing


class MagneticFieldFromRing:
    def __init__(self, ring: SegmentedRing, current: float) -> None:
        self.ring = ring
        self.current = current

    def __call__(self, point: np.ndarray) -> np.ndarray:
        distances = point - self.ring.points

        coefficient = np.pow(np.linalg.norm(distances, axis=1), -3) * self.current
        direction = np.cross(self.ring.dl, distances)

        return np.sum(coefficient[:, np.newaxis] * direction, axis=0)
