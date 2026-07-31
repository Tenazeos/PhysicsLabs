import numpy as np
import streamlit as st

from ..calculations import ElectricFieldStrength
from ..model import Capacitor


@st.cache_data(show_spinner=False)
def get_raw_slice_data(
    capacitor: Capacitor, _field: ElectricFieldStrength, grid_coords: np.ndarray, coef: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    point_grid = grid_coords + np.array([[0, 0, capacitor.distance * coef]])
    vector_grid = np.array([_field(point) for point in point_grid])

    v, u, w = vector_grid[:, 0], vector_grid[:, 1], vector_grid[:, 2]
    return u, v, w
