import numpy as np
from scipy.integrate import ode

from ..models import MagneticTrap, Particle, State
from .magnetic_field import MagneticFieldFromRing


class MovementProcessor:
    def __init__(self, trap: MagneticTrap, particle: Particle, start_state: State) -> None:
        self.trap = trap
        self.current_state = start_state

        self.upper_field = MagneticFieldFromRing(trap.upper_ring, trap.current_strength)
        self.lower_field = MagneticFieldFromRing(trap.lower_ring, trap.current_strength)

        self.inner_coefficient_ = particle.charge / particle.weight

        self.ode = ode(
            f=self.inner_,
        ).set_initial_value(self.current_state.velocity)

    def inner_(self, _time: float, velocity: np.ndarray) -> np.ndarray:
        magnetic_induction = self.lower_field(self.current_state.position) + self.upper_field(
            self.current_state.position
        )

        return np.cross(velocity, magnetic_induction) * self.inner_coefficient_

    def process(self, time_delta: float) -> None:
        new_velocity = self.ode.integrate(self.ode.t + time_delta)
        new_position = self.current_state.position + new_velocity * time_delta

        self.current_state = State(
            position=new_position,
            velocity=new_velocity,
        )

    def get_state(self) -> State:
        return self.current_state
