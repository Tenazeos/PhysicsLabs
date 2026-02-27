from copy import copy

import numpy as np

from labs.the_capacitor.model import RectCapacitor, RectPlate


def extract_central_rect(
    capacitor: RectCapacitor, charge: np.ndarray
) -> tuple[RectCapacitor, np.ndarray, np.ndarray]:
    """
    Extracts the central area (1/2 of the shortest side) of the capacitor and the corresponding
    charge distribution. Plates should be the same size (to avoid flow shift).
    """
    new_plate_side = min(capacitor.lower_plate.length, capacitor.lower_plate.width) / 2
    new_chunk_count = int(new_plate_side // capacitor.chunk_side)

    plate = RectPlate.from_square(side=new_plate_side, chunk_side=capacitor.chunk_side)
    new_capacitor = RectCapacitor(
        lower_plate=plate,
        upper_plate=copy(plate),
        distance=capacitor.distance,
        voltage=capacitor.voltage,
    )

    lower_plate_charge = charge[: capacitor.lower_plate.chunk_count].reshape(
        capacitor.lower_plate.length_chunk_count, capacitor.lower_plate.width_chunk_count
    )
    upper_plate_charge = charge[capacitor.lower_plate.chunk_count :].reshape(
        capacitor.upper_plate.length_chunk_count, capacitor.upper_plate.width_chunk_count
    )

    length_offset = int(capacitor.lower_plate.length_chunk_count - new_chunk_count) // 2
    width_offset = int(capacitor.lower_plate.width_chunk_count - new_chunk_count) // 2

    # fmt: off
    new_lower_plate_charge = lower_plate_charge[
        length_offset : length_offset + new_chunk_count,
        width_offset : width_offset + new_chunk_count
    ]
    new_upper_plate_charge = upper_plate_charge[
        length_offset : length_offset + new_chunk_count,
        width_offset : width_offset + new_chunk_count
    ]
    return new_capacitor, new_lower_plate_charge.flatten(), new_upper_plate_charge.flatten()
