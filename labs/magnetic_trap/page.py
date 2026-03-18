import streamlit as st
import numpy as np
import plotly.express as px


from .models import MagneticTrap, SegmentedRing, State, Particle
from .calculations import MovementProcessor


def page() -> None:
    st.write("Debug")

    distances = st.sidebar.slider("Distance between ring", 1.0, 10.0, 2.0)
    radius = st.sidebar.slider("Radius of ring", 1.0, 10.0, 2.0)
    strength = st.sidebar.slider("Current strength of ring", 1.0, 10.0, 2.0)
    segment_count = st.sidebar.slider("Number of segments", 10, 100, 20)

    weight = st.sidebar.slider("Weight of particle", 1.0, 10.0, 2.0)
    charge = st.sidebar.slider("Charge of particle", 1.0, 10.0, 2.0)

    is_run = st.sidebar.button("Run")

    if is_run:
        trap = MagneticTrap(
            upper_ring=SegmentedRing(
                radius=radius,
                segment_count=segment_count,
                z_cord=distances,
            ),
            lower_ring=SegmentedRing(
                radius=radius,
                segment_count=segment_count,
                z_cord=0,
            ),
            current_strength=strength,
        )

        start_state = State(
            position=np.array([0.0, 0.0, distances / 2]),
            velocity=np.array([1.0, 1.0, 0.01]),
        )

        movement = MovementProcessor(
            trap=trap,
            particle=Particle(
                weight=weight,
                charge=charge,
            ),
            start_state=start_state,
        )

        states = []
        time_delta = 0.1

        for i in range(100):
            movement.process(time_delta)

            state = movement.get_state()
            states.append({
                "x": state.position[0],
                "y": state.position[1],
                "z": state.position[2],
            })

        fig = px.scatter_3d(
            states,
            x='x',
            y='y',
            z='z',
            size_max=10,
            opacity=0.7
        )

        fig.update_layout(
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z"
            ),
            width=800,
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)
