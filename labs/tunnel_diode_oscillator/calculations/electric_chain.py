# ruff: noqa: N806

from scipy.integrate import ode

from ..model import Settings, State


class ElectricChain:
    settings: Settings

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        self.ode = (
            ode(f=self.__calculation_step)
            .set_initial_value(y=[0, 0], t=0.0)
            .set_integrator(name="vode", method="bdf", atol=1e-6, rtol=1e-4, max_step=1e-10)
        )

    def __calculation_step(self, _: float, state: list[float]) -> list[float]:
        amperage, voltage = state

        dI = self.settings.electromotive_force - amperage * self.settings.resistance - voltage
        dI /= self.settings.inductance

        dU = amperage - self.settings.diode.amperage(voltage)
        dU /= self.settings.capacity

        return [dI, dU]

    def step(self, time_delta: float) -> State:
        amperage, voltage = self.ode.integrate(self.ode.t + time_delta)
        return State(amperage, voltage)
