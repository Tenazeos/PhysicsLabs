from dataclasses import dataclass

from labs.model.vector import Vector3D


@dataclass(slots=True)
class Molecule:
    velocity: Vector3D
    position: Vector3D
