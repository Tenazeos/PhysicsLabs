from labs.model.vector import Vector3D
from labs.perfect_gas.model import Molecule


def collide_mollecules(
    first: Molecule, second: Molecule, normal: Vector3D, molecule_radius: float
) -> None:
    projection_first = normal * (normal @ first.velocity)
    projection_second = normal * (normal @ second.velocity)

    complement_first = first.velocity - projection_first
    complement_second = second.velocity - projection_second

    first.velocity = complement_first + projection_second
    second.velocity = complement_second + projection_first

    overlap = 2 * molecule_radius - (first.position - second.position).norm
    if overlap > 0:
        separation = normal * (overlap * 0.5)
        first.position -= separation
        second.position += separation
