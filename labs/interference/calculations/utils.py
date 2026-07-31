import numpy as np


def generate_meshgrid(
    width: float, height: float, points_by_height_axis: int = 1000
) -> tuple[np.ndarray, np.ndarray]:
    x = np.linspace(-width / 2, width / 2, int(points_by_height_axis * width / height))
    y = np.linspace(-height / 2, height / 2, points_by_height_axis)
    return np.meshgrid(x, y)
