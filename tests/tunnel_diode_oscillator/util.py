import math
import statistics


def get_mean_and_normalized(voltages: list[float]) -> tuple[float, list[float]]:
    mean_v = statistics.mean(voltages)
    norm_v = [v - mean_v for v in voltages]
    return mean_v, norm_v


def find_amplitude(norm_voltages: list[float]) -> float:
    return max(abs(v) for v in norm_voltages)


def find_zero_crossings(times: list[float], norm_voltages: list[float]) -> list[float]:
    crossings = []
    for i in range(1, len(norm_voltages)):
        v1, v2 = norm_voltages[i - 1], norm_voltages[i]
        if v1 * v2 <= 0 and v1 != v2:
            t1, t2 = times[i - 1], times[i]
            t_cross = t1 - v1 * (t2 - t1) / (v2 - v1)
            crossings.append(t_cross)
    return crossings


def calculate_period(crossings: list[float]) -> float:
    if len(crossings) >= 3:
        periods = [crossings[i + 2] - crossings[i] for i in range(len(crossings) - 2)]
        return sum(periods) / len(periods)
    if len(crossings) >= 2:
        return 2 * (crossings[1] - crossings[0])
    return 1.0


def calculate_phase(times: list[float], norm_voltages: list[float], r: float, k: float) -> float:
    if r > 0:
        max_idx = norm_voltages.index(max(norm_voltages))
        t_max = times[max_idx]
        return math.pi / 2 - k * t_max
    return 0.0


def extract_sine_params(
    times: list[float], voltages: list[float]
) -> tuple[float, float, float, float]:
    mean_v, norm_v = get_mean_and_normalized(voltages)
    r = find_amplitude(norm_v)
    crossings = find_zero_crossings(times, norm_v)
    period = calculate_period(crossings)

    k = 2 * math.pi / period if period > 0 else 1.0
    phase = calculate_phase(times, norm_v, r, k)

    return mean_v, r, k, phase
