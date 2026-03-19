import numpy as np
import plotly.express as px
import streamlit as st

from .calculations import MovementProcessor
from .models import MagneticTrap, Particle, SegmentedRing, State

TIME_DELTA = 0.01
FRAME_COUNT = 1000
RING_SEGMENT_COUNT = 50

SI_TO_SGSM_COEF = 0.1  # for amperes and coulombs


def page() -> None:
    st.set_page_config(page_title="Magnetic trap 🧲", page_icon="🧲", layout="wide")

    st.title("Magnetic trap 🧲")

    with st.sidebar:
        ring_radius = st.slider(
            "Ring radius (cm)",
            min_value=1.0,
            max_value=10.0,
            value=4.0,
            step=0.01,
        )
        ring_distance = st.slider(
            "Distance between rings (cm)",
            min_value=1.0,
            max_value=10.0,
            value=4.0,
            step=0.01,
        )
        ring_current = (
            st.slider(
                "Electric current in rings (A)",
                min_value=1.0,
                max_value=10.0,
                value=5.0,
                step=0.01,
            )
            * SI_TO_SGSM_COEF
        )

        particle_mass = (
            st.slider(
                "Particle mass (mg)",
                min_value=10.0,
                max_value=1000.0,
                value=100.0,
                step=0.1,
            )
            / 1000
        )
        particle_charge = (
            st.slider(
                "Particle charge (C)",
                min_value=-10.0,
                max_value=10.0,
                value=3.0,
                step=0.01,
            )
            * SI_TO_SGSM_COEF
        )
        particle_launch_angle = st.slider(
            "Particle launch angle (deg)",
            min_value=-90.0,
            max_value=90.0,
            value=-30.0,
            step=0.1,
        )

    center_between_rings = np.array([0, 0, ring_distance / 2])
    particle_velocity_norm = 1
    particle_velocity = np.array(
        [
            -particle_velocity_norm * np.cos(particle_launch_angle) / np.sqrt(2),
            particle_velocity_norm * np.cos(particle_launch_angle) / np.sqrt(2),
            particle_velocity_norm * np.sin(particle_launch_angle),
        ]
    )

    movement = MovementProcessor(
        trap=MagneticTrap(
            upper_ring=SegmentedRing(
                radius=ring_radius,
                z_cord=ring_distance,
                segment_count=RING_SEGMENT_COUNT,
            ),
            lower_ring=SegmentedRing(
                radius=ring_radius,
                z_cord=0,
                segment_count=RING_SEGMENT_COUNT,
            ),
            current=ring_current,
        ),
        particle=Particle(
            mass=particle_mass,
            charge=particle_charge,
        ),
        start_state=State(
            position=center_between_rings,
            velocity=particle_velocity,
        ),
    )

    states = [movement.state]
    for _ in range(FRAME_COUNT):
        movement.process(TIME_DELTA)
        states.append(movement.state)

    fig = px.scatter_3d(
        [
            {
                "x": state.position[0],
                "y": state.position[1],
                "z": state.position[2],
            }
            for state in states
        ],
        x="x",
        y="y",
        z="z",
        size_max=10,
        opacity=0.7,
    )

    fig.update_layout(
        scene={"xaxis_title": "X", "yaxis_title": "Y", "zaxis_title": "Z"},
        width=800,
        height=600,
    )

    st.plotly_chart(fig, width="stretch")
