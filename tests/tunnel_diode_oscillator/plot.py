import math

import matplotlib.pyplot as plt

from labs.tunnel_diode_oscillator.calculations.electric_chain import ElectricChain
from labs.tunnel_diode_oscillator.model.diode import TunnelDiode
from labs.tunnel_diode_oscillator.model.settings import Settings
from tests.tunnel_diode_oscillator.util import extract_sine_params


def run_and_plot():
    settings = Settings(
        resistance=0.5, capacity=1e-8, inductance=1e-5, electromotive_force=1.0, diode=TunnelDiode()
    )

    time_step = 1e-7
    end_time = 300 * time_step

    chain = ElectricChain(settings)
    t = 0.0
    times = []
    voltages = []
    amperages = []

    while t <= end_time:
        state = chain.step(time_step)
        t += time_step
        times.append(t)
        voltages.append(state.voltage)
        amperages.append(state.amperage)

    mean_v, r, k, phase = extract_sine_params(times, voltages)
    u_approx = [mean_v + r * math.sin(k * t_val + phase) for t_val in times]

    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.plot(times, voltages, label="U (actual)", color="blue", linewidth=2)
    ax1.plot(
        times, u_approx, label="U_approx (ideal sine)", color="green", linestyle=":", linewidth=2
    )
    ax1.set_title("Voltage Comparison (U vs U_approx)")
    ax1.set_xlabel("Time (t)")
    ax1.set_ylabel("Voltage (U)")
    ax1.legend()
    ax1.grid(visible=True)

    ax2.plot(times, amperages, label="I (actual)", color="red", linewidth=2)
    ax2.set_title("Amperage Check")
    ax2.set_xlabel("Time (t)")
    ax2.set_ylabel("Amperage (I)")
    ax2.legend()
    ax2.grid(visible=True)

    plt.tight_layout()
    plt.show()


# uv run python -m tests.tunnel_diode_oscillator.plot
if __name__ == "__main__":
    run_and_plot()
