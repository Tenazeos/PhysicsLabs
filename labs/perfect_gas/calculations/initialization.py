# ruff: noqa: S311
import random
from collections.abc import Generator

from labs.model.vector import Vector2D

from ..model import Container, Molecule


def create_all_molecules_at_the_bottom(
    container: Container, count: int, max_velocity: float
) -> Generator[Molecule, None, None]:
    for _ in range(count):
        yield Molecule(
            position=Vector2D(
                x=random.uniform(0, container.width),
                y=0 + random.random(),
            ),
            velocity=Vector2D(
                x=random.uniform(-max_velocity, max_velocity),
                y=random.uniform(-max_velocity, max_velocity),
            ),
        )
