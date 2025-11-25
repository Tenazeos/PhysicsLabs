import streamlit as st

from .calculations import Calculator, create_all_molecules_at_the_bottom
from .model.container import Container


def page() -> None:
    st.title("Perfect Gas [DEBUG]")

    radius = st.sidebar.slider("Radius", 1.0, 10.0, 5.0)
    velocity = st.sidebar.slider("Velocity", 0.0, 100.0, 10.0)

    height = st.sidebar.slider("Height", 50.0, 500.0, 200.0)
    width = st.sidebar.slider("Width", 50.0, 500.0, 200.0)

    container = Container(height=height, width=width)

    calculator: Calculator = Calculator(
        molecules_gen=create_all_molecules_at_the_bottom(
            container=container,
            count=10,
            max_velocity=velocity,
        ),
        container=container,
        molecules_radius=radius,
    )

    print(calculator)
