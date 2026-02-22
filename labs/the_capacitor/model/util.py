from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from .state import Capacitor, Plate


def generate_capacitor_chunks_vector(capacitor: "Capacitor") -> np.ndarray:
    upper_plate = _generate_plate_vector(capacitor.upper_plate, capacitor.distance)
    lower_plate = _generate_plate_vector(capacitor.lower_plate, 0.0)
    return np.vstack([lower_plate, upper_plate])


def _generate_plate_vector(plate: "Plate", z_coord: float) -> np.ndarray:
    x_coords = np.arange(plate.length_chunk_count) * plate.chunk_side + (plate.chunk_side / 2)
    y_coords = np.arange(plate.width_chunk_count) * plate.chunk_side + (plate.chunk_side / 2)

    # Create the 2D grid
    xv, yv = np.meshgrid(x_coords, y_coords)

    # Add z-axis and flatten
    grid = np.stack([xv, yv, np.full_like(xv, z_coord)], axis=-1)
    return grid.reshape(-1, 3)
