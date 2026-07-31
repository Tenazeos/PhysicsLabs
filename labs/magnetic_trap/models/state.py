from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class State:
    position: np.ndarray
    velocity: np.ndarray
