from labs.model.constant import GAS_CONSTANT, g
from labs.perfect_gas.model import Container, Experiment, Molecule

from ...model.vector import Vector3D
from .collision import collide_mollecules
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
        enable_gravity: bool,  # noqa
    ) -> None:
        self.container = container
        self.settings = settings
        self.molecules = list(generator)

        self.enable_gravity = enable_gravity

        self.delta_vel_per_wall = {
            "x+": 0.0,
            "x-": 0.0,
            "y+": 0.0,
            "y-": 0.0,
            "z+": 0.0,
            "z-": 0.0,
        }

        self.current_time = 0.0

        self.hit_with_wall_count = 0
        self.hit_inner_count = 0

    def step(self, time_delta: float) -> None:
        self._process_movement(time_delta)
        self._process_container_collisions()
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
                molecule.velocity.x *= -1
                molecule.position.x = self.settings.radius

                self.hit_with_wall_count += 1
            elif molecule.position.x + self.settings.radius >= self.container.length:
                self.delta_vel_per_wall["x+"] += abs(molecule.velocity.x)
                molecule.velocity.x *= -1
                molecule.position.x = self.container.length - self.settings.radius

                self.hit_with_wall_count += 1

            if molecule.position.y - self.settings.radius <= 0:
                self.delta_vel_per_wall["y-"] += abs(molecule.velocity.y)
                molecule.velocity.y *= -1
                molecule.position.y = self.settings.radius

                self.hit_with_wall_count += 1
            elif molecule.position.y + self.settings.radius >= self.container.width:
                self.delta_vel_per_wall["y+"] += abs(molecule.velocity.y)
                molecule.velocity.y *= -1
                molecule.position.y = self.container.width - self.settings.radius

                self.hit_with_wall_count += 1

            if molecule.position.z - self.settings.radius <= 0:
                self.delta_vel_per_wall["z-"] += abs(molecule.velocity.z)
                molecule.velocity.z *= -1
                molecule.position.z = self.settings.radius

                self.hit_with_wall_count += 1
            elif molecule.position.z + self.settings.radius >= self.container.height:
                self.delta_vel_per_wall["z+"] += abs(molecule.velocity.z)
                molecule.velocity.z *= -1
                molecule.position.z = self.container.height - self.settings.radius

                self.hit_with_wall_count += 1

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

        # millikelvins
        return self.settings.molar_mass * average_square_velocity / (3 * GAS_CONSTANT)

    @property
    def pressure(self) -> float:
        pressures = {
            "x+": self.delta_vel_per_wall["x+"]
            * self.settings.molar_mass
            / SPECIAL_AVOGADRO
            / self.current_time
            / (self.container.height * self.container.width),
            "x-": self.delta_vel_per_wall["x-"]
            * self.settings.molar_mass
            / SPECIAL_AVOGADRO
            / self.current_time
            / (self.container.height * self.container.width),
            "y+": self.delta_vel_per_wall["y+"]
            * self.settings.molar_mass
            / SPECIAL_AVOGADRO
            / self.current_time
            / (self.container.length * self.container.height),
            "y-": self.delta_vel_per_wall["y-"]
            * self.settings.molar_mass
            / SPECIAL_AVOGADRO
            / self.current_time
            / (self.container.length * self.container.height),
            "z+": self.delta_vel_per_wall["z+"]
            * self.settings.molar_mass
            / SPECIAL_AVOGADRO
            / self.current_time
            / (self.container.length * self.container.width),
            "z-": self.delta_vel_per_wall["z-"]
            * self.settings.molar_mass
            / SPECIAL_AVOGADRO
            / self.current_time
            / (self.container.length * self.container.width),
        }

        # millipascals
        return (
            10
            * (
                pressures["x+"]
                + pressures["x-"]
                + pressures["y+"]
                + pressures["y-"]
                + pressures["z+"]
                + pressures["z-"]
            )
            / 6
        )
