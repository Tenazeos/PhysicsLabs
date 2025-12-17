# ruff: noqa: S311
import random
from collections.abc import Generator

from labs.model.vector import Vector3D

from ..model import Container, Molecule

StartStateGenerator = Generator[Molecule, None, None]


def random_place(
    min_velocity: float, max_velocity: float, number: int, container: Container
) -> StartStateGenerator:
    for _ in range(number):
        yield Molecule(
            velocity=Vector3D(
                x=random.uniform(min_velocity, max_velocity) * random.choice((-1, 1)),
                y=random.uniform(min_velocity, max_velocity) * random.choice((-1, 1)),
                z=random.uniform(min_velocity, max_velocity) * random.choice((-1, 1)),
            ),
            position=Vector3D(
                x=random.uniform(0, container.length),
                y=random.uniform(0, container.width),
                z=random.uniform(0, container.height),
            ),
        )
