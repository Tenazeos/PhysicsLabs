# ruff: noqa: RUF001

from __future__ import annotations

from math import cos, exp, sin, sqrt

from labs.model.constant import g
from labs.swing_the_pendulum.model import PendulumState

from .data import NO_FRICTION, SAMPLING_DELTA, SIMULATION_TIME


def run_theoretical_simulation(
    pendulum: PendulumState,
    *,
    friction_coefficient: float = NO_FRICTION,
    sampling_delta: float = SAMPLING_DELTA,
    simulation_time: float = SIMULATION_TIME,
) -> tuple[list[PendulumState], list[PendulumState]]:
    time = 0.0
    states = [pendulum]
    extremes = [pendulum]

    initial_angle = pendulum.angle
    initial_angular_velocity = pendulum.angular_velocity

    while time <= simulation_time:
        angle = calculate_angle_with_friction(
            time,
            pendulum.length,
            pendulum.weight,
            friction_coefficient,
            initial_angle,
            initial_angular_velocity,
        )

        angular_velocity = (
            calculate_angle_with_friction(
                time + sampling_delta,
                pendulum.length,
                pendulum.weight,
                friction_coefficient,
                initial_angle,
                initial_angular_velocity,
            )
            - angle
        ) / sampling_delta

        state = PendulumState(
            length=pendulum.length,
            weight=pendulum.weight,
            angle=angle,
            angular_velocity=angular_velocity,
            time=time,
        )

        if (
            len(states) >= 2
            and (states[-1].angle - states[-2].angle) * (state.angle - states[-1].angle) < 0
        ):
            extremes.append(states[-1])

        states.append(state)
        time += sampling_delta

    return states, extremes


def calculate_angle_with_friction(
    t: float,
    length: float,
    weight: float,
    friction_coefficient: float,
    initial_angle: float,
    initial_angular_velocity: float,
) -> float:
    """
    Вычисляет угол отклонения маятника в момент времени t при наличии трения.

    Для случая γ < 1:
    φ(t) = e^(-γω₀t) * (C₁cos(ω_d t) + C₂sin(ω_d t))

    где:
    C₁ = φ₀
    C₂ = (φ'₀ + γω₀φ₀) / ω_d
    """
    natural_angular_frequency = calculate_natural_angular_frequency(length)
    gamma_coef = calculate_gamma(friction_coefficient, length, weight)

    if gamma_coef >= 1:
        raise ValueError(f"γ = {gamma_coef} >= 1, требуется γ < 1 для периодических колебаний")

    damped_angular_frequency = calculate_damped_angular_frequency(
        natural_angular_frequency, gamma_coef
    )

    c1 = initial_angle
    c2 = (
        initial_angular_velocity + gamma_coef * natural_angular_frequency * initial_angle
    ) / damped_angular_frequency

    return exp(-gamma_coef * natural_angular_frequency * t) * (
        c1 * cos(damped_angular_frequency * t) + c2 * sin(damped_angular_frequency * t)
    )


def calculate_natural_angular_frequency(length: float) -> float:
    """
    Вычисляет собственную частоту колебаний без трения.

    ω₀ = √(3g/(2L))
    """
    return sqrt(3 * g / (2 * length))


def calculate_gamma(friction_coefficient: float, length: float, weight: float) -> float:
    """
    Вычисляет коэффициент затухания.

    γ = βL/(2mω₀) = βL/(2m) * √(2L/(3g))
    """
    natural_angular_frequency = calculate_natural_angular_frequency(length)
    return friction_coefficient * length / (2 * weight * natural_angular_frequency)


def calculate_damped_angular_frequency(natural_angular_frequency: float, gamma: float) -> float:
    """
    Вычисляет частоту затухающих колебаний.

    ω_d = ω₀√(1-γ²)
    """
    return natural_angular_frequency * sqrt(1 - gamma * gamma)
