from collections.abc import Generator

from labs.model.vector import Vector2D
from labs.perfect_gas.model import Container, Molecule


class Calculator:
    def __init__(
        self,
        molecules_gen: Generator[Molecule, None, None],
        container: Container,
        molecules_radius: float,
    ) -> None:
        self.molecules = list(molecules_gen)
        self.container = container
        self.molecules_radius = molecules_radius

    def step(self, time_delta: float) -> None:
        self.__updates_positions(time_delta)
        self.__check_collisions_with_container()
        self.__check_inner_collisions()

    def __updates_positions(self, time_delta: float) -> None:
        for i in range(len(self.molecules)):
            self.molecules[i].position += self.molecules[i].velocity * time_delta

    def __check_collisions_with_container(self) -> None:
        for i in range(len(self.molecules)):
            if self.molecules[i].position.x < self.molecules_radius:
                self.molecules[i].position.x = self.molecules_radius
                self.molecules[i].velocity.x *= -1
            elif self.molecules[i].position.x > self.container.width - self.molecules_radius:
                self.molecules[i].position.x = self.container.width - self.molecules_radius
                self.molecules[i].velocity.x *= -1

            if self.molecules[i].position.y < self.molecules_radius:
                self.molecules[i].position.y = self.molecules_radius
                self.molecules[i].velocity.y *= -1
            elif self.molecules[i].position.y > self.container.height - self.molecules_radius:
                self.molecules[i].position.y = self.container.height - self.molecules_radius
                self.molecules[i].velocity.y *= -1

    def __check_inner_collisions(self) -> None:
        for i in range(len(self.molecules)):
            for j in range(i, len(self.molecules)):
                distance: Vector2D = self.molecules[i].position - self.molecules[j].position

                if 0 < distance.norm < self.molecules_radius * 2:
                    normal = distance / distance.norm

                    projection_i = normal * (self.molecules[i].velocity @ normal)
                    projection_j = normal * (self.molecules[j].velocity @ normal)

                    self.molecules[i].velocity += -projection_i + projection_j
                    self.molecules[j].velocity += -projection_j + projection_i

                    overlap = self.molecules_radius * 2 - distance.norm
                    self.molecules[i].position -= distance * (overlap / 2)
                    self.molecules[j].position += distance * (overlap / 2)
