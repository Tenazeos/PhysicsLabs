import streamlit as st
from matplotlib import pyplot as plt

from .calculations import get_interference_figure
from .models import Screen, Settings


def page() -> None:
    st.header("Interference")

    settings = Settings(
        screen=Screen(
            z_position=st.sidebar.slider(
                "Расстояние от щелей до экрана, м", min_value=0.0, max_value=10.0, value=1.0
            ),
            width=st.sidebar.slider("Ширина экрана, мм", min_value=1.0, max_value=100.0) * 1e-3,
            height=st.sidebar.slider("Высота экрана, мм", min_value=1.0, max_value=100.0) * 1e-3,
        ),
        distance_between_slits=st.sidebar.slider(
            "Расстояние между щелями, мм", min_value=0.1, max_value=10.0, value=0.5
        )
        * 1e-3,
        wavelength=st.sidebar.slider("Длина волны, нм", min_value=400, max_value=760) * 1e-9,
    )

    image = get_interference_figure(settings)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(image, cmap="inferno", interpolation="auto")
    st.pyplot(fig)
