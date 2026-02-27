import numpy as np

from labs.the_capacitor.model import DiskCapacitor, DiskPlate


def extract_central_disk(
    capacitor: DiskCapacitor, charge: np.ndarray
) -> tuple[DiskCapacitor, np.ndarray, np.ndarray]:
    central_radius = capacitor.lower_plate.radius / 2

    new_lower_plate = DiskPlate(radius=central_radius, dr=capacitor.lower_plate.dr)
    new_upper_plate = DiskPlate(radius=central_radius, dr=capacitor.upper_plate.dr)

    new_capacitor = DiskCapacitor(
        lower_plate=new_lower_plate,
        upper_plate=new_upper_plate,
        distance=capacitor.distance,
        voltage=capacitor.voltage,
    )

    lower_count = capacitor.lower_plate.chunk_count
    new_lower_count = new_capacitor.lower_plate.chunk_count

    lower_charge = charge[:lower_count]
    upper_charge = charge[lower_count:]

    new_lower_charge = lower_charge[:new_lower_count]
    new_upper_charge = upper_charge[:new_lower_count]

    return new_capacitor, new_lower_charge, new_upper_charge
