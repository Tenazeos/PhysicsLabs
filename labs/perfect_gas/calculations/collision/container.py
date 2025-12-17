from __future__ import annotations

import numpy as np

from labs.model.vector import Vector3D
from labs.perfect_gas.model import Molecule
from labs.perfect_gas.model.container import Wall


def collide_with_wall(wall: Wall, molecule: Molecule, molecule_mass: float) -> None:
    local_wall_velocity = get_randomized_velocity(wall)
    previous_molecule_velocity = molecule.velocity
    molecule.velocity = molecule.velocity + 2 * local_wall_velocity

    transfered_energy = (
        molecule_mass * (molecule.velocity.norm**2 - previous_molecule_velocity.norm**2) / 2
    )
    wall.energy -= transfered_energy


def get_randomized_velocity(wall: Wall) -> Vector3D:
    return np.sin(np.random.uniform(0.0, 2 * np.pi)) * wall.velocity
