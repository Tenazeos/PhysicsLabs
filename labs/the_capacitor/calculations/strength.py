import numpy as np

from labs.the_capacitor.calculations.charge import calculate_charge

from ..model import Capacitor


class ElectricFieldStrength:
    """Represents the electric field strength of a capacitor."""

    def __init__(self, capacitor: Capacitor) -> None:
        self.capacitor = capacitor
        self.charge = calculate_charge(capacitor)

    def __call__(self, point: np.ndarray) -> np.ndarray:
        distances = self.capacitor.chunks_vector - point
        strength_norm = np.pow(np.linalg.norm(distances, axis=1), -3) * self.charge

        return np.sum(strength_norm[:, np.newaxis] * distances, axis=0)
