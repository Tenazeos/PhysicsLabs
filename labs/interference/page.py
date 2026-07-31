import numpy as np
import streamlit as st
from matplotlib import colormaps

from .calculations import calculate_visibility, get_interference_figure
from .models import Screen, Settings


def page() -> None:
    st.set_page_config(page_title="Interference 💡", page_icon="💡", layout="wide")

    st.title("Interference 💡")

    with st.sidebar:
        settings = Settings(
            screen=Screen(
                z_position=st.slider(
                    "Screen distance (m)",
                    min_value=0.1,
                    max_value=10.0,
                    value=1.0,
                ),
                width=(
                    st.slider(
                        "Screen width (mm)",
                        min_value=1.0,
                        max_value=100.0,
                        value=10.0,
                    )
                    * 1e-3
                ),
                height=(
                    st.slider(
                        "Высота height (mm)",
                        min_value=1.0,
                        max_value=100.0,
                        value=5.0,
                    )
                    * 1e-3
                ),
            ),
            distance_between_slits=(
                st.slider(
                    "Distance between slits (mm)",
                    min_value=0.1,
                    max_value=10.0,
                    value=1.0,
                )
                * 1e-3
            ),
            wavelength=(
                st.slider(
                    "Wavelength (nm)",
                    min_value=380,
                    max_value=750,
                    value=520,
                )
                * 1e-9
            ),
        )

    intensity_figure = get_interference_figure(settings)
    st.image(
        colormaps.get_cmap("inferno")(
            (intensity_figure - np.min(intensity_figure))
            / (np.max(intensity_figure) - np.min(intensity_figure))
        ),
        caption="Intensity (interference pattern)",
    )

    with st.container(horizontal=True, horizontal_alignment="center"):
        st.metric(
            "Fringe visibility",
            f"{calculate_visibility(intensity_figure):.2%}",
            width="content",
        )
