from dataclasses import dataclass

from .diode import Diode


@dataclass(slots=True)
class Settings:
    resistance: float
    capacity: float
    inductance: float
    electromotive_force: float
    diode: Diode
