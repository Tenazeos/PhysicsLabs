import numpy as np


def generate_meshgrid(
    width: float, height: float, points_by_axis: int = 1000
) -> tuple[np.ndarray, np.ndarray]:
    x = np.linspace(-width / 2, height / 2, points_by_axis)
    y = np.linspace(-width / 2, height / 2, points_by_axis)
    return np.meshgrid(x, y)
