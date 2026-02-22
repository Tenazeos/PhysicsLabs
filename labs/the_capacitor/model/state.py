from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

import numpy as np

from labs.the_capacitor.calculations.util import generate_capacitor_chunks_vectors


@dataclass
class Capacitor:
    lower_plate: Plate
    upper_plate: Plate

    distance: float
    voltage: float

    @cached_property
    def chunk_vectors(self) -> np.ndarray:
        return generate_capacitor_chunks_vectors(self)


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
