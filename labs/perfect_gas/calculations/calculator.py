from labs.model.constant import GAS_CONSTANT, g
from labs.perfect_gas.model import Container, Experiment, Molecule
from labs.perfect_gas.model.container import Wall
from labs.perfect_gas.model.orientation import SurfacePosition

from ...model.vector import Vector3D
from .collision import collide_mollecules, collide_with_wall
from .initialization import StartStateGenerator

# avogadro without exp
SPECIAL_AVOGADRO = 6.022


class Calculator:
    container: Container
    settings: Experiment
    molecules: list[Molecule]

    def __init__(
        self,
        container: Container,
        settings: Experiment,
        generator: StartStateGenerator,
        *,
        enable_gravity: bool,
        enable_internal_collisions: bool,
    ) -> None:
        self.container = container
        self.settings = settings
        self.molecules = list(generator)
        self.molecule_mass = settings.molar_mass / (1e23 * SPECIAL_AVOGADRO)  # grams

        self.enable_gravity = enable_gravity
        self.enable_internal_collisions = enable_internal_collisions

        self.delta_vel_per_wall = {
            "x+": 0.0,
            "x-": 0.0,
            "y+": 0.0,
            "y-": 0.0,
            "z+": 0.0,
            "z-": 0.0,
        }

        z_size = container.height
        y_size = container.width
        x_size = container.length
        self.walls: dict[SurfacePosition, Wall] = {
            "x+": Wall(area=y_size * z_size, position="x+"),
            "x-": Wall(area=y_size * z_size, position="x-"),
            "y+": Wall(area=x_size * z_size, position="y+"),
            "y-": Wall(area=x_size * z_size, position="y-"),
            "z+": Wall(area=x_size * y_size, position="z+"),
            "z-": Wall(area=x_size * y_size, position="z-"),
        }

        self.current_time = 0.0

        self.hit_with_wall_count = 0
        self.hit_inner_count = 0

    def step(self, time_delta: float) -> None:
        self._process_movement(time_delta)
        self._process_container_collisions()

        if self.enable_internal_collisions:
            self._process_inner_collision()

        self.current_time += time_delta

    def _process_movement(self, time_delta: float) -> None:
        for molecule in self.molecules:
            if self.enable_gravity:
                # gravity in nanometer per nanosecond in square
                molecule.velocity += (
                    Vector3D(
                        x=0.0,
                        y=0.0,
                        z=-(g * 1e-9),
                    )
                    * time_delta
                )
            molecule.position += molecule.velocity * time_delta

    def _process_container_collisions(self) -> None:
        for molecule in self.molecules:
            if molecule.position.x - self.settings.radius <= 0:
                self.delta_vel_per_wall["x-"] += abs(molecule.velocity.x)
                self.hit_with_wall_count += 1

                collide_with_wall(self.walls["x-"], molecule, self.molecule_mass)
                molecule.position.x = self.settings.radius

            elif molecule.position.x + self.settings.radius >= self.container.length:
                self.delta_vel_per_wall["x+"] += abs(molecule.velocity.x)
                self.hit_with_wall_count += 1

                collide_with_wall(self.walls["x+"], molecule, self.molecule_mass)
                molecule.position.x = self.container.length - self.settings.radius

            if molecule.position.y - self.settings.radius <= 0:
                self.delta_vel_per_wall["y-"] += abs(molecule.velocity.y)
                self.hit_with_wall_count += 1

                collide_with_wall(self.walls["y-"], molecule, self.molecule_mass)
                molecule.position.y = self.settings.radius

            elif molecule.position.y + self.settings.radius >= self.container.width:
                self.delta_vel_per_wall["y+"] += abs(molecule.velocity.y)
                self.hit_with_wall_count += 1

                collide_with_wall(self.walls["y+"], molecule, self.molecule_mass)
                molecule.position.y = self.container.width - self.settings.radius

            if molecule.position.z - self.settings.radius <= 0:
                self.delta_vel_per_wall["z-"] += abs(molecule.velocity.z)
                self.hit_with_wall_count += 1

                collide_with_wall(self.walls["z-"], molecule, self.molecule_mass)
                molecule.position.z = self.settings.radius

            elif molecule.position.z + self.settings.radius >= self.container.height:
                self.delta_vel_per_wall["z+"] += abs(molecule.velocity.z)
                self.hit_with_wall_count += 1

                collide_with_wall(self.walls["z+"], molecule, self.molecule_mass)
                molecule.position.z = self.container.height - self.settings.radius

    def _process_inner_collision(self) -> None:
        for i in range(len(self.molecules)):
            for j in range(i + 1, len(self.molecules)):
                mol1 = self.molecules[i]
                mol2 = self.molecules[j]

                delta_pos = mol2.position - mol1.position
                distance = delta_pos.norm

                if 0 < distance < 2 * self.settings.radius:
                    normal = delta_pos / distance
                    if (mol2.velocity - mol1.velocity) @ normal > 0:
                        continue

                    collide_mollecules(mol1, mol2, normal, self.settings.radius)
                    self.hit_inner_count += 1

    @property
    def temperature(self) -> float:
        average_square_velocity: float = 0.0

        for molecule in self.molecules:
            average_square_velocity += molecule.velocity.norm**2

        average_square_velocity /= len(self.molecules)

        # kelvins
        return self.settings.molar_mass * average_square_velocity / (3 * GAS_CONSTANT) / 1e3

    @property
    def pressures(self) -> dict[str, float]:
        # Pa * 10^-2
        pressures = {
            "x+": (
                self.delta_vel_per_wall["x+"]
                * self.settings.molar_mass
                / SPECIAL_AVOGADRO
                / self.current_time
                / (self.container.height * self.container.width)
            ),
            "x-": (
                self.delta_vel_per_wall["x-"]
                * self.settings.molar_mass
                / SPECIAL_AVOGADRO
                / self.current_time
                / (self.container.height * self.container.width)
            ),
            "y+": (
                self.delta_vel_per_wall["y+"]
                * self.settings.molar_mass
                / SPECIAL_AVOGADRO
                / self.current_time
                / (self.container.length * self.container.height)
            ),
            "y-": (
                self.delta_vel_per_wall["y-"]
                * self.settings.molar_mass
                / SPECIAL_AVOGADRO
                / self.current_time
                / (self.container.length * self.container.height)
            ),
            "z+": (
                self.delta_vel_per_wall["z+"]
                * self.settings.molar_mass
                / SPECIAL_AVOGADRO
                / self.current_time
                / (self.container.length * self.container.width)
            ),
            "z-": (
                self.delta_vel_per_wall["z-"]
                * self.settings.molar_mass
                / SPECIAL_AVOGADRO
                / self.current_time
                / (self.container.length * self.container.width)
            ),
        }

        return {
            "top": pressures["z+"] / 1e2,
            "bottom": pressures["z-"] / 1e2,
            "sides": (
                (pressures["x+"] + pressures["x-"] + pressures["y+"] + pressures["y-"]) / 4 / 1e2
            ),
        }
