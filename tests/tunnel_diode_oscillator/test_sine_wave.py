import math

from labs.tunnel_diode_oscillator.calculations.electric_chain import ElectricChain
from labs.tunnel_diode_oscillator.model.diode import TunnelDiode
from labs.tunnel_diode_oscillator.model.settings import Settings
from tests.tunnel_diode_oscillator.util import extract_sine_params


def _collect_data(
    settings: Settings, time_step: float, end_time: float
) -> tuple[list[float], list[float]]:
    chain = ElectricChain(settings)
    t = 0.0
    times = []
    voltages = []

    while t <= end_time:
        state = chain.step(time_step)
        t += time_step
        times.append(t)
        voltages.append(state.voltage)

    return times, voltages


def test_is_sine_wave():
    settings = Settings(
        resistance=0.5, capacity=1e-8, inductance=1e-5, electromotive_force=1.0, diode=TunnelDiode()
    )

    time_step = 1e-7
    end_time = 300 * time_step

    times, voltages = _collect_data(settings, time_step, end_time)
    mean_v, r, k, phase = extract_sine_params(times, voltages)

    for t, v in zip(times, voltages, strict=True):
        expected = mean_v + r * math.sin(k * t + phase)
        assert math.isclose(v, expected, rel_tol=0.1, abs_tol=r * 0.15), (
            f"Mismatch at t={t}: {v} != {expected}"
        )
