__all__ = ["pages"]

import streamlit as st

from .flight_to_mars import page as flight_to_mars_page
from .interference import page as interference_page
from .magnetic_trap import page as magnetic_trap_page
from .roll_the_ball import page as roll_the_ball_page
from .swing_the_pendulum import page as swing_the_pendulum_page
from .the_capacitor import page as the_capacitor_page
from .throw_a_rock import page as throw_a_rock_page
from .tunnel_diode_oscillator import page as tunnel_diode_oscillator_page

pages = {
    "Autumn semester": [
        st.Page(
            throw_a_rock_page,
            title="Throw a rock",
            icon="🪨",
            url_path="throw-a-rock",
        ),
        st.Page(
            flight_to_mars_page,
            title="Flight to Mars",
            icon="🚀",
            url_path="flight-to-mars",
        ),
        st.Page(
            roll_the_ball_page,
            title="Roll the ball",
            icon="⚽",
            url_path="roll-the-ball",
        ),
        st.Page(
            swing_the_pendulum_page,
            title="Swing the pendulum",
            icon="🦯",
            url_path="swing-the-pendulum",
        ),
    ],
    "Spring semester": [
        st.Page(
            the_capacitor_page,
            title="The capacitor",
            icon="⚡️",
            url_path="the-capacitor",
        ),
        st.Page(
            magnetic_trap_page,
            title="Magnetic trap",
            icon="🧲",
            url_path="magnetic-trap",
        ),
        st.Page(
            tunnel_diode_oscillator_page,
            title="Tunnel diode oscillator",
            icon="🔃",
            url_path="tunnel-diode-oscillator",
        ),
        st.Page(
            interference_page,
            title="Interference",
            url_path="interference",
        ),
    ],
}
