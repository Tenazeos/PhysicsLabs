# ruff: noqa: RUF001
import streamlit as st
from plotly import express as px

from labs.model.constant import g
from labs.util.formatting import scientific_superscript, superscript_digits

from .calculations import Calculator, random_place
from .calculations.calculator import SPECIAL_AVOGADRO
from .model import Experiment
from .model.container import Container


def page() -> None:
    st.set_page_config(page_title="Perfect Gas ☁", page_icon="☁", layout="wide")

    st.title("Perfect Gas ☁️")

    with st.sidebar:
        molecule_count = st.slider(
            "Number of molecules",
            min_value=500,
            max_value=5000,
            value=1000,
        )

        with st.container(horizontal=True, horizontal_alignment="distribute"):
            concentration = st.slider(
                "Gas concentration, per m³",
                min_value=0.01,
                max_value=10.0,
                step=0.01,
                format="%.2f",
                value=1.0,
            )
            concentration_exponent = st.selectbox(
                "<no label>",
                options=range(21, 28),
                index=4,  # ^24
                format_func=lambda exp: f"×10{str(exp).translate(superscript_digits)}",
                label_visibility="hidden",
                width=100,
            )

        experiment = Experiment(
            molar_mass=st.slider(
                "Molar mass, g/mol",
                min_value=1,
                max_value=50,
                value=4,
            ),
            radius=st.slider(
                "Molecule radius, nm",
                min_value=0.1,
                max_value=10.0,
                step=0.01,
                format="%.2f",
                value=0.14,
            ),
            number=molecule_count,
        )

        min_velocity, max_velocity = st.slider(
            "Initial molecule velocity range (per axis), m/s",
            min_value=100.0,
            max_value=2000.0,
            step=0.1,
            format="%.1f",
            value=(600.0, 900.0),
        )

        container_side_ratio = st.slider(
            "Container side ratio",
            min_value=0.1,
            max_value=10.0,
            step=0.1,
            format="%.1f",
            value=1.0,
            help="Height to base side length",
        )

        enable_gravity = st.checkbox("Enable gravity", value=True)
        enable_internal_collisions = st.checkbox("Enable internal collisions", value=False)

        steps = st.slider(
            "Simulation steps",
            min_value=100,
            max_value=10000,
            value=1000,
            step=100,
        )

        run_simulation = st.button(
            "Run simulation",
            type="primary",
            width="stretch",
        )

        # in nm³
        volume = (molecule_count / concentration) * (10 ** (27 - concentration_exponent))
        base_length = (volume / container_side_ratio) ** (1 / 3)
        container = Container(
            length=base_length,
            width=base_length,
            height=base_length * container_side_ratio,
        )

        time_delta = 2 * experiment.radius / max_velocity  # in nanoseconds

        with st.expander("Calculated parameters", expanded=True):
            st.html(f"Container base side length: <b>{container.length:.2f} nm</b>")
            st.html(f"Container height: <b>{container.height:.2f} nm</b>")
            st.html(f"Container volume: <b>{scientific_superscript(volume)} nm³</b>")

        with st.expander("Constants used"):
            st.html(f"g = {g} m/s<sup>2</sup>")
            st.html(f"N<sub>A</sub> = {SPECIAL_AVOGADRO}×10<sup>23</sup> molecules/mol")

    calculator: Calculator = Calculator(
        container=container,
        settings=experiment,
        generator=random_place(min_velocity, max_velocity, experiment.number, container),
        enable_gravity=enable_gravity,
        enable_internal_collisions=enable_internal_collisions,
    )

    if run_simulation:
        st.html(
            f"Optimal time delta: <b>{scientific_superscript(time_delta)} ns</b> <br>"
            f"Total time: <b>{scientific_superscript(time_delta * steps)} ns</b>"
        )

        start_heights = calculator.get_molecule_heights()
        start_speeds_x = calculator.get_molecule_speeds_x()
        start_speeds_y = calculator.get_molecule_speeds_y()

        progress_bar = st.progress(0)
        status_text = st.empty()

        for step in range(steps):
            calculator.step(time_delta)
            progress_bar.progress((step + 1) / steps)
            status_text.text(f"Шаг: {step + 1}/{steps}")

        with st.container(horizontal=True, horizontal_alignment="center", gap="large"):
            st.metric(
                "Temperature",
                f"{calculator.temperature:.2f} K",
                width="content",
            )

            st.metric(
                "Collisions with walls",
                calculator.hit_with_wall_count,
                width="content",
            )
            st.metric(
                "Internal collisions",
                calculator.hit_inner_count,
                width="content",
            )

        with st.container(horizontal=True, horizontal_alignment="center", gap="large"):
            for side, pressure in calculator.pressures.items():
                st.metric(
                    f"Pressure: {side}",
                    f"{pressure:.2f} Pa",
                    width="content",
                )

        hist_col1, hist_col2 = st.columns(2)

        with hist_col1:
            st.subheader("At the start")

            figure = px.histogram(
                x=start_speeds_x,
                nbins=60,
                color_discrete_sequence=["#1f77b4"],
                title="Maxwell distribution (X)",
                labels={"x": "X velocity, m/s", "y": "Count"},
            )
            figure.update_layout(showlegend=False, bargap=0.1)
            st.plotly_chart(figure, key="start_x")

            figure = px.histogram(
                x=start_speeds_y,
                nbins=60,
                color_discrete_sequence=["#00bb54"],
                title="Maxwell distribution (Y)",
                labels={"x": "Y velocity, m/s", "y": "Count"},
            )
            figure.update_layout(showlegend=False, bargap=0.1)
            st.plotly_chart(figure, key="start_y")

            figure = px.histogram(
                x=start_heights,
                nbins=60,
                color_discrete_sequence=["#ff7f0e"],
                title="Boltzmann distribution",
                labels={"x": "Z coordinate, nm", "y": "Count"},
            )
            figure.update_layout(showlegend=False, bargap=0.1)
            st.plotly_chart(figure, key="start_z")

        with hist_col2:
            st.subheader("At the end")

            figure = px.histogram(
                x=calculator.get_molecule_speeds_x(),
                nbins=60,
                color_discrete_sequence=["#1f77b4"],
                title="Maxwell distribution (X)",
                labels={"x": "X velocity, m/s", "y": "Count"},
            )
            figure.update_layout(showlegend=False, bargap=0.1)
            st.plotly_chart(figure, key="end_x")

            figure = px.histogram(
                x=calculator.get_molecule_speeds_y(),
                nbins=60,
                color_discrete_sequence=["#00bb54"],
                title="Maxwell distribution (Y)",
                labels={"x": "Y velocity, m/s", "y": "Count"},
            )
            figure.update_layout(showlegend=False, bargap=0.1)
            st.plotly_chart(figure, key="end_y")

            figure = px.histogram(
                x=calculator.get_molecule_heights(),
                nbins=60,
                color_discrete_sequence=["#ff7f0e"],
                title="Boltzmann distribution",
                labels={"x": "Z coordinate, nm", "y": "Count"},
            )
            figure.update_layout(showlegend=False, bargap=0.1)
            st.plotly_chart(figure, key="end_z")
