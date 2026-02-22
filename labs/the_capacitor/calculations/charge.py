from __future__ import annotations

import numpy as np
from scipy import linalg, spatial

from ..model import Capacitor


def calculate_charge(capacitor: Capacitor) -> np.ndarray:
    """
    Calculate the charge on each particle given the distance matrix and the state of the system.

    :return: Charges on each chunk in the same order as the chunks vector.
    """
    chunks = capacitor.chunk_vectors
    n = chunks.shape[0]

    distances = spatial.distance_matrix(chunks, chunks)
    numerator = np.ones_like(distances) - np.eye(n)
    denominator = distances + np.eye(n)
    inversed_distances = numerator / denominator

    voltage = (chunks[:, 2] > 0) * capacitor.voltage
    return linalg.solve(inversed_distances, voltage)
