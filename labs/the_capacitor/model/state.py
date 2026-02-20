from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Capacitor:
    lower_plate: Plate
    upper_plate: Plate

    distance: float
    voltage: float


@dataclass
class Plate:
    length: float
    width: float
    chunk_side: float

    @property
    def length_chunk_count(self) -> int:
        return int(self.length // self.chunk_side)

    @property
    def width_chunk_count(self) -> int:
        return int(self.width // self.chunk_side)
