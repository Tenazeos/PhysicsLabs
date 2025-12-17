from __future__ import annotations

import numpy as np

from labs.model.vector import Vector3D
from labs.perfect_gas.model import Molecule
from labs.perfect_gas.model.container import Wall


def collide_with_wall(wall: Wall, molecule: Molecule, molar_mass: float) -> None:
    local_wall_velocity = get_randomized_velocity(wall)
    if local_wall_velocity.norm:
        share_energy(local_wall_velocity, wall, molecule, molar_mass)
    else:
        heat_the_wall(wall, molecule, molar_mass)


def share_energy(
    local_wall_velocity: Vector3D, wall: Wall, molecule: Molecule, molar_mass: float
) -> None:
    previous_molecule_velocity = molecule.velocity

    main_projection = (molecule.velocity @ wall.surface_norm) * wall.surface_norm
    complement = molecule.velocity - main_projection

    new_molecule_velocity = 2 * local_wall_velocity - main_projection + complement
    transfered_energy = (
        molar_mass * (molecule.velocity.norm**2 - previous_molecule_velocity.norm**2) / 2
    )

    if transfered_energy > wall.energy:
        heat_the_wall(wall, molecule, molar_mass)

    wall.energy -= transfered_energy
    molecule.velocity = new_molecule_velocity


def heat_the_wall(wall: Wall, molecule: Molecule, molar_mass: float) -> None:
    main_projection = (molecule.velocity @ wall.surface_norm) * wall.surface_norm

    molecule.velocity -= main_projection

    main_energy = main_projection.norm**2 * molar_mass / 2
    wall.energy += main_energy


def get_randomized_velocity(wall: Wall) -> Vector3D:
    return np.sin(np.random.uniform(0.0, 2 * np.pi)) * wall.velocity
