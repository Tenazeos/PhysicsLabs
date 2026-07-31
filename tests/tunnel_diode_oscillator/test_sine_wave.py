import math

from labs.tunnel_diode_oscillator.calculations.electric_chain import ElectricChain
from labs.tunnel_diode_oscillator.model.diode import TunnelDiode
from labs.tunnel_diode_oscillator.model.settings import Settings
from labs.tunnel_diode_oscillator.page import dynamic_sampling_delta
from tests.tunnel_diode_oscillator.util import extract_sine_params

settings = Settings(
    resistance=40,
    capacity=1e-7,
    inductance=1e-3,
    electromotive_force=1.5,
    diode=TunnelDiode(),
)


def _collect_data(
    settings: Settings,
    time_step: float,
    start_time: float,
    end_time: float,
) -> tuple[list[float], list[float]]:
    chain = ElectricChain(settings)
    t = 0.0
    times = []
    voltages = []

    while t <= end_time:
        state = chain.step(time_step)
        t += time_step

        if t >= start_time:
            times.append(t)
            voltages.append(state.voltage)

    return times, voltages


def test_is_sine_wave():
    time_step = dynamic_sampling_delta(settings)
    start_time = 500 * time_step  # some offset for stabilization
    end_time = start_time + 300 * time_step

    times, voltages = _collect_data(settings, time_step, start_time, end_time)
    mean_v, r, k, phase = extract_sine_params(times, voltages)

    for t, v in zip(times, voltages, strict=True):
        expected = mean_v + r * math.sin(k * t + phase)
        assert math.isclose(v, expected, rel_tol=0.1, abs_tol=r * 0.15), (
            f"Mismatch at t={t}: {v} != {expected}"
        )
