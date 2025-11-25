from dataclasses import dataclass

from labs.model.vector import Vector2D


@dataclass(slots=True)
class Molecule:
    velocity: Vector2D
    position: Vector2D
