from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from labs.model.vector import Vector3D

from .orientation import SurfacePosition, surface_norm_by_position


@dataclass(frozen=True)
class Container:
    length: float
    height: float
    width: float


@dataclass
class Wall:
    area: float
    position: SurfacePosition
    mass: float = 1  # gramms
    energy: float = 0  # milijoules / mole

    @property
    def velocity(self) -> Vector3D:
        return np.sqrt(2 * self.energy / self.mass) * self.surface_norm

    @property
    def surface_norm(self) -> Vector3D:
        return surface_norm_by_position[self.position]
