import copy

from labs.model.constant import GAS_CONSTANT, g
from labs.perfect_gas.model import Container, Experiment, Molecule, SystemState

from ...model.vector import Vector3D
from .initialization import StartStateGenerator

# avogadro without exp
SPECIAL_AVOGADRO = 6.022


class Calculator:
    container: Container
    settings: Experiment
    molecules: list[Molecule]
    current_state: SystemState

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

        self.current_state = SystemState(temperature=self._calculate_temperature(), pressure=0.0)

    def step(self, time_delta: float) -> None:
        self._process_movement(time_delta)
        delta_vel = self._process_container_collisions()
        self._process_inner_collision()

        self.current_state = SystemState(
            temperature=self._calculate_temperature(),
            pressure=self._calculate_pressure(time_delta, delta_vel),
        )

    def get_state(self) -> SystemState:
        return copy.copy(self.current_state)

    def _process_movement(self, time_delta: float) -> None:
        for molecule in self.molecules:
            if self.enable_gravity:
                molecule.velocity += (
                    Vector3D(
                        x=0.0,
                        y=0.0,
                        z=-(g * 1e-9),
                    )
                    * time_delta
                )
            molecule.position += molecule.velocity * time_delta

    def _process_container_collisions(self) -> dict[str, float]:
        delta_vel = {"x+": 0.0, "x-": 0.0, "y+": 0.0, "y-": 0.0, "z+": 0.0, "z-": 0.0}

        for molecule in self.molecules:
            if molecule.position.x - self.settings.radius <= 0:
                delta_vel["x-"] += abs(molecule.velocity.x)
                molecule.velocity.x *= -1
                molecule.position.x = self.settings.radius
            elif molecule.position.x + self.settings.radius >= self.container.length:
                delta_vel["x+"] += abs(molecule.velocity.x)
                molecule.velocity.x *= -1
                molecule.position.x = self.container.length - self.settings.radius

            if molecule.position.y - self.settings.radius <= 0:
                delta_vel["y-"] += abs(molecule.velocity.y)
                molecule.velocity.y *= -1
                molecule.position.y = self.settings.radius
            elif molecule.position.y + self.settings.radius >= self.container.width:
                delta_vel["y+"] += abs(molecule.velocity.y)
                molecule.velocity.y *= -1
                molecule.position.y = self.container.width - self.settings.radius

            if molecule.position.z - self.settings.radius <= 0:
                delta_vel["z-"] += abs(molecule.velocity.z)
                molecule.velocity.z *= -1
                molecule.position.z = self.settings.radius
            elif molecule.position.z + self.settings.radius >= self.container.height:
                delta_vel += abs(molecule.velocity.z)
                molecule.velocity.z *= -1
                molecule.position.z = self.container.height - self.settings.radius

        return delta_vel

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

                    projection_first = normal * (normal @ mol1.velocity)
                    projection_second = normal * (normal @ mol2.velocity)

                    complement_first = mol1.velocity - projection_first
                    complement_second = mol2.velocity - projection_second

                    mol1.velocity = complement_first + projection_second
                    mol2.velocity = complement_second + projection_first

                    overlap = 2 * self.settings.radius - distance
                    if overlap > 0:
                        separation = normal * (overlap * 0.5)
                        mol1.position -= separation
                        mol2.position += separation

    def _calculate_temperature(self) -> float:
        average_square_velocity: float = 0.0

        for molecule in self.molecules:
            average_square_velocity += molecule.velocity.norm**2

        average_square_velocity /= len(self.molecules)

        # millikelvins
        return self.settings.molar_mass * average_square_velocity / (3 * GAS_CONSTANT)

    def _calculate_pressure(self, time_delta: float, delta_vel: dict[str, float]) -> float:
        pressures = {
            "x+": delta_vel["x+"]
            * self.settings.molar_mass
            / SPECIAL_AVOGADRO
            / time_delta
            / (self.container.height * self.container.width),
            "x-": delta_vel["x-"]
            * self.settings.molar_mass
            / SPECIAL_AVOGADRO
            / time_delta
            / (self.container.height * self.container.width),
            "y+": delta_vel["y+"]
            * self.settings.molar_mass
            / SPECIAL_AVOGADRO
            / time_delta
            / (self.container.length * self.container.height),
            "y-": delta_vel["y-"]
            * self.settings.molar_mass
            / SPECIAL_AVOGADRO
            / time_delta
            / (self.container.length * self.container.height),
            "z+": delta_vel["z+"]
            * self.settings.molar_mass
            / SPECIAL_AVOGADRO
            / time_delta
            / (self.container.length * self.container.width),
            "z-": delta_vel["z-"]
            * self.settings.molar_mass
            / SPECIAL_AVOGADRO
            / time_delta
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
