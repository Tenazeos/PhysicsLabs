from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

import numpy as np

from .util.rect import generate_rect_capacitor_chunks_vector


@dataclass
class RectCapacitor:
    lower_plate: RectPlate
    upper_plate: RectPlate

    distance: float
    voltage: float

    def __post_init__(self) -> None:
        if self.lower_plate.chunk_side != self.upper_plate.chunk_side:
            raise ValueError("Chunk sides of upper and lower plates must be the same")

    @property
    def chunk_side(self) -> float:
        return self.lower_plate.chunk_side

    @cached_property
    def chunks_vector(self) -> np.ndarray:
        return generate_rect_capacitor_chunks_vector(self)


@dataclass
class RectPlate:
    length: float
    width: float
    chunk_side: float

    @classmethod
    def from_square(cls, side: float, chunk_side: float) -> RectPlate:
        return cls(length=side, width=side, chunk_side=chunk_side)

    @property
    def length_chunk_count(self) -> int:
        return int(self.length // self.chunk_side)

    @property
    def width_chunk_count(self) -> int:
        return int(self.width // self.chunk_side)

    @property
    def chunk_count(self) -> int:
        return self.length_chunk_count * self.width_chunk_count

    @property
    def area(self) -> float:
        return self.length * self.width
