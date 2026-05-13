import numpy as np

from labs.interference.calculations.calculation import get_interference_figure
from labs.interference.models.settings import Screen, Settings


def test_interference_symmetry():
    settings = Settings(
        screen=Screen(z_position=1.0, width=0.1, height=0.1),
        distance_between_slits=0.001,
        wavelength=500e-9,
    )
    figure = get_interference_figure(settings)

    assert np.allclose(figure, np.fliplr(figure))
    assert np.allclose(figure, np.flipud(figure))


def test_theoretical_fringe_positions():
    """Проверка совпадения позиций максимумов с теорией"""
    settings = Settings(
        screen=Screen(z_position=2.0, width=0.01, height=0.01),
        distance_between_slits=0.001,
        wavelength=500e-9,
    )
    figure = get_interference_figure(settings)
    center_y, center_x = figure.shape[0] // 2, figure.shape[1] // 2

    # Теоретическое расстояние между максимумами: Delta x = lambda * L / d
    fringe_width = (
        settings.wavelength * settings.screen.z_position
    ) / settings.distance_between_slits
    dx = settings.screen.width / figure.shape[1]

    pixels_to_max = int(fringe_width / dx)
    pixels_to_min = int(fringe_width / dx / 2)

    first_side_max_idx = center_x + pixels_to_max
    first_min_idx = center_x + pixels_to_min

    assert figure[center_y, first_side_max_idx] > figure[center_y, first_min_idx]
    np.testing.assert_allclose(
        figure[center_y, center_x],
        figure[center_y, first_side_max_idx],
        rtol=1e-3,
        err_msg="Интенсивность побочного max должна быть близка к центральному при малых углах",
    )


def test_intensity_profile_paraxial_approximation():
    """Сравниваем с аналитической формулой (I ~ I0 * cos^2) в параксиальном приближении"""
    settings = Settings(
        screen=Screen(z_position=5.0, width=0.02, height=0.02),
        distance_between_slits=0.001,
        wavelength=600e-9,
    )
    points_by_axis = 1000
    figure = get_interference_figure(settings)
    center_y = points_by_axis // 2

    numerical_profile = figure[center_y, :]
    x = np.linspace(-settings.screen.width / 2, settings.screen.width / 2, points_by_axis)

    # I(x) = I_max * cos^2(pi * x * d / (lambda * L))
    phase_diff = (
        np.pi
        * settings.distance_between_slits
        * x
        / (settings.wavelength * settings.screen.z_position)
    )
    analytical_profile = np.cos(phase_diff) ** 2

    numerical_norm = numerical_profile / np.max(numerical_profile)
    np.testing.assert_allclose(numerical_norm, analytical_profile, atol=1e-2)
