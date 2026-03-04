import numpy as np

from ..models import SegmentedRing


class MagneticFieldFromRing:
    def __init__(self, ring: SegmentedRing, current_strength: float) -> None:
        self.ring = ring
        self.current_strength = current_strength

    def __call__(self, point: np.ndarray) -> np.ndarray:
        distances = point - self.ring.points

        coefficient = np.pow(np.linalg.norm(distances, axis=1), -3) * self.current_strength
        direction = np.cross(self.ring.dl, distances)

        return np.sum(coefficient[:, np.newaxis] * direction, axis=0)
