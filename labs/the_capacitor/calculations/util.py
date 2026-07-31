import numpy as np

from ..model import Capacitor


def measure_capacity(capacitor: Capacitor, charge: np.ndarray) -> float:
    """Численное измерение емкости конденсатора по распределению зарядов на его пластинах."""
    return abs(np.sum(charge[: capacitor.lower_plate.chunk_count])) / capacitor.voltage
