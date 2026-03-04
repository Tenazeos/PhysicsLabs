from dataclasses import dataclass


@dataclass(frozen=True)
class Particle:
    weight: float
    charge: float
