import numpy as np

from labs.the_capacitor.model import Capacitor


def evaluate_capacity(capacitor: Capacitor) -> float:
    """Returns the theoretical capacity of the capacitor."""
    # epsilon_0 = 8.854187817e-12  # Vacuum permittivity in F/m
    epsilon_0 = 1 / (4 * np.pi)  # В СГС
    area = capacitor.lower_plate.length * capacitor.lower_plate.width
    return epsilon_0 * area / capacitor.distance
