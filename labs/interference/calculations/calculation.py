import numpy as np

from ..models import Settings
from .utils import generate_meshgrid


def get_interference_figure(settings: Settings) -> np.ndarray:
    k = 2 * np.pi / settings.wavelength

    x, y = generate_meshgrid(settings.screen.width, settings.screen.height)

    r1 = np.sqrt(
        (x - settings.distance_between_slits / 2) ** 2 + y**2 + settings.screen.z_position**2
    )
    r2 = np.sqrt(
        (x + settings.distance_between_slits / 2) ** 2 + y**2 + settings.screen.z_position**2
    )

    intensity_from_first = np.exp(1j * k * r1) / r1
    intensity_from_second = np.exp(1j * k * r2) / r2

    return np.abs(intensity_from_first + intensity_from_second) ** 2


def calculate_visibility(intensity_figure: np.ndarray) -> float:
    i_max = np.max(intensity_figure)
    i_min = np.min(intensity_figure)
    if abs(i_max + i_min) <= 1e-9:
        return 0.0
    return float((i_max - i_min) / (i_max + i_min))
