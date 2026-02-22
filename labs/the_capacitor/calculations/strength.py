import numpy as np

from ..model import Capacitor


class ElectricFieldStrength:
    """Represents the electric field strength of a capacitor."""

    def __init__(self, capacitor: Capacitor, charge: np.ndarray) -> None:
        self.capacitor = capacitor
        self.charge = charge

    def __call__(self, point: np.ndarray) -> np.ndarray:
        distances = self.capacitor.chunks_vector - point
        strength_norm = np.pow(np.linalg.norm(distances, axis=1), -3) * self.charge

        return np.sum(strength_norm[:, np.newaxis] * distances, axis=0)
