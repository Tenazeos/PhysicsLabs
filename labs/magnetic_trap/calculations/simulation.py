import numpy as np
from scipy.integrate import ode

from ..models import MagneticTrap, Particle, State
from .magnetic_field import MagneticFieldFromRing


class MovementProcessor:
    def __init__(self, trap: MagneticTrap, particle: Particle, start_state: State) -> None:
        self.trap = trap
        self.state = start_state

        self.upper_field = MagneticFieldFromRing(trap.upper_ring, trap.current)
        self.lower_field = MagneticFieldFromRing(trap.lower_ring, trap.current)

        self._inner_coefficient = particle.charge / particle.mass

        self.ode = ode(f=self._inner).set_initial_value(self.state.velocity)

    def _inner(self, _time: float, velocity: np.ndarray) -> np.ndarray:
        magnetic_induction = self.lower_field(self.state.position) + self.upper_field(
            self.state.position
        )
        return np.cross(velocity, magnetic_induction) * self._inner_coefficient

    def process(self, time_delta: float) -> None:
        new_velocity = self.ode.integrate(self.ode.t + time_delta)
        new_position = self.state.position + new_velocity * time_delta

        self.state = State(
            position=new_position,
            velocity=new_velocity,
        )
