from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Container:
    length: float
    height: float
    width: float


@dataclass
class Wall:
    mass: float
    energy: float
    area: float

    @property
    def velocity(self) -> float:
        return np.sqrt(2 * self.energy / self.mass)
