from dataclasses import dataclass
from typing import Any

from .diode import Diode


@dataclass
class Settings:
    resistance: float
    capacity: float
    inductance: float
    electromotive_force: float
    diode: Diode

    @property
    def _value_tuple(self) -> tuple[float, float, float, float]:
        return self.resistance, self.capacity, self.inductance, self.electromotive_force

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Settings):
            return NotImplemented

        return self._value_tuple == other._value_tuple

    def __hash__(self) -> int:
        return hash(self._value_tuple)
