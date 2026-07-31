from dataclasses import dataclass


@dataclass(frozen=True)
class Particle:
    mass: float
    charge: float
