import numpy as np
import streamlit as st

from .calculations import MovementProcessor
from .models import MagneticTrap, Particle, SegmentedRing, State
from .visualization.animation import render_particle_animation

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

        st.space()

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
        particle_start_offset = st.slider(
            "Particle start offset [horizontal] (cm)",
            min_value=0.0,
            max_value=10.0,
            value=3.0,
            step=0.01,
        )
        particle_velocity = st.slider(
            "Particle velocity (cm/s)",
            min_value=-5.0,
            max_value=5.0,
            value=1.5,
            step=0.01,
        )
        particle_launch_pitch = np.radians(
            st.slider(
                "Particle launch vertical angle [pitch] (deg)",
                min_value=-90.0,
                max_value=90.0,
                value=30.0,
                step=0.1,
            )
        )
        particle_launch_yaw = np.radians(
            st.slider(
                "Particle launch horizontal angle [yaw] (deg)",
                min_value=-90.0,
                max_value=90.0,
                value=00.0,
                step=0.1,
            )
        )

    center_between_rings = np.array([0, particle_start_offset, ring_distance / 2])
    initial_particle_velocity_vector = np.array(
        [
            -particle_velocity * np.cos(particle_launch_pitch) * np.sin(particle_launch_yaw),
            -particle_velocity * np.cos(particle_launch_pitch) * np.cos(particle_launch_yaw),
            particle_velocity * np.sin(particle_launch_pitch),
        ]
    )

    trap = MagneticTrap(
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
    )
    movement = MovementProcessor(
        trap=trap,
        particle=Particle(
            mass=particle_mass,
            charge=particle_charge,
        ),
        start_state=State(
            position=center_between_rings,
            velocity=initial_particle_velocity_vector,
        ),
    )

    states = [movement.state]
    for _ in range(FRAME_COUNT):
        movement.process(TIME_DELTA)
        states.append(movement.state)

    st.plotly_chart(
        render_particle_animation(
            trap=trap, initial_velocity=initial_particle_velocity_vector, states=states
        )
    )
    st.markdown(
        "<p style='text-align: center; color: #888888;'>"
        "Sadly, the point of view resets when clicking <b>Play</b> button."
        "</p>",
        unsafe_allow_html=True,
    )
