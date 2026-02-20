import numpy as np

from ..model import Capacitor
from .util import generate_capacitor_plates_vector


class ElectricFieldStrength:
    """Represents the electric field strength of a capacitor."""

    def __init__(self, charge: np.ndarray, capacitor: Capacitor) -> None:
        self.charge = charge
        self.chunk_coordinates = generate_capacitor_plates_vector(capacitor)

    def __call__(self, point: np.ndarray) -> np.ndarray:
        distance = self.chunk_coordinates - point

        strength_norm = np.pow(np.linalg.norm(distance, axis=1), -3) * self.charge

        return np.sum(strength_norm[:, np.newaxis] * distance, axis=0)
