from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..disk import DiskCapacitor, DiskPlate


def generate_disk_capacitor_chunks_vector(capacitor: "DiskCapacitor") -> np.ndarray:
    upper_plate = generate_disk_plate_vector(
        capacitor.upper_plate.radius, capacitor.upper_plate.dr, capacitor.distance
    )
    lower_plate = generate_disk_plate_vector(
        capacitor.lower_plate.radius, capacitor.lower_plate.dr, 0.0
    )
    return np.vstack([lower_plate, upper_plate])


def generate_disk_plate_vector(radius: float, dr: float, z_coord: float) -> np.ndarray:
    points = [[0.0, 0.0, z_coord]]
    n = int(radius / dr)
    for i in range(1, n + 1):
        r = i * dr
        n_points = int(np.round(2 * np.pi * r / dr))
        angles = np.linspace(0, 2 * np.pi, n_points, endpoint=False)
        x = r * np.cos(angles)
        y = r * np.sin(angles)
        z = np.full_like(x, z_coord)
        points.extend(np.column_stack((x, y, z)))
    return np.array(points)


def count_disk_plate_charges(plate: "DiskPlate") -> int:
    n = int(plate.radius / plate.dr)
    return 1 + sum(int(np.round(2 * np.pi * i)) for i in range(1, n + 1))
