# ruff: noqa: RUF001
import math
from dataclasses import asdict, dataclass
from enum import Enum

import streamlit as st

from labs.util.formatting import superscript_digits

from .calculations import ElectricChain
from .model import Settings, TunnelDiode
from .visualization import render_phase_portrait

type ScientificPair = tuple[float, int]  # float * 10^(int)

POINTS_PER_PERIOD = 50
PERIODS_PER_CHUNK = 6
POINTS_PER_CHUNK = POINTS_PER_PERIOD * PERIODS_PER_CHUNK


def dynamic_sampling_delta(settings: Settings) -> float:
    return 2 * math.pi * math.sqrt(settings.inductance * settings.capacity) / POINTS_PER_PERIOD


@dataclass
class ParameterPresetData:
    resistance: ScientificPair
    capacity: ScientificPair
    inductance: ScientificPair
    electromotive_force: ScientificPair


class ParameterPreset(Enum):
    GENERATION = ParameterPresetData(
        resistance=(4.0, 1),
        capacity=(1.0, -7),
        inductance=(1.0, -3),
        electromotive_force=(1.5, 0),
    )
    WARPED = ParameterPresetData(
        resistance=(5.0, 1),
        capacity=(0.5, -8),
        inductance=(1.0, -3),
        electromotive_force=(1.5, 0),
    )
    FADING = ParameterPresetData(
        resistance=(5.0, -1),
        capacity=(1.0, -8),
        inductance=(1.0, -5),
        electromotive_force=(2.0, 0),
    )


def apply_preset() -> None:
    selected_preset: ParameterPreset = st.session_state.preset_selector

    for parameter, (value, power) in asdict(selected_preset.value).items():
        st.session_state[f"{parameter}_slider"] = value
        st.session_state[f"{parameter}_power"] = power


def page() -> None:
    st.set_page_config(page_title="Tunnel diode oscillator 🔃", page_icon="🔃", layout="wide")

    with st.container(horizontal=True, horizontal_alignment="distribute"):
        st.title("Tunnel diode oscillator 🔃")
        simulate_further = st.button("Simulate further", type="primary")

    with st.sidebar:
        st.segmented_control(
            "Parameter preset",
            options=list(ParameterPreset),
            default=ParameterPreset.GENERATION,
            format_func=lambda preset: preset.name.replace("_", " ").capitalize(),
            required=True,
            width="stretch",
            key="preset_selector",
            on_change=apply_preset,
        )
        if "parameter_preset_applied" not in st.session_state:
            st.session_state.parameter_preset_applied = True
            apply_preset()

        with st.container(horizontal=True, horizontal_alignment="distribute"):
            resistance = st.slider(
                "Resistance (Ω)", min_value=0.01, max_value=10.0, step=0.01, key="resistance_slider"
            ) * 10 ** st.selectbox(
                "<power>",
                options=range(-3, 4),
                format_func=lambda exp: f"×10{str(exp).translate(superscript_digits)}",
                label_visibility="hidden",
                width=100,
                key="resistance_power",
            )

        with st.container(horizontal=True, horizontal_alignment="distribute"):
            capacity = st.slider(
                "Capacity (F)", min_value=0.01, max_value=10.0, step=0.01, key="capacity_slider"
            ) * 10 ** st.selectbox(
                "<power>",
                options=range(-10, -5),
                format_func=lambda exp: f"×10{str(exp).translate(superscript_digits)}",
                label_visibility="hidden",
                width=100,
                key="capacity_power",
            )

        with st.container(horizontal=True, horizontal_alignment="distribute"):
            inductance = st.slider(
                "Inductance (H)", min_value=0.01, max_value=10.0, step=0.01, key="inductance_slider"
            ) * 10 ** st.selectbox(
                "<power>",
                options=range(-6, -1),
                format_func=lambda exp: f"×10{str(exp).translate(superscript_digits)}",
                label_visibility="hidden",
                width=100,
                key="inductance_power",
            )

        with st.container(horizontal=True, horizontal_alignment="distribute"):
            electromotive_force = st.slider(
                "Electromotive force (V)",
                min_value=0.01,
                max_value=10.0,
                step=0.01,
                key="electromotive_force_slider",
            ) * 10 ** st.selectbox(
                "<power>",
                options=range(-3, 4),
                format_func=lambda exp: f"×10{str(exp).translate(superscript_digits)}",
                label_visibility="hidden",
                width=100,
                key="electromotive_force_power",
            )

    settings = Settings(
        resistance=resistance,
        capacity=capacity,
        inductance=inductance,
        electromotive_force=electromotive_force,
        diode=TunnelDiode(),
    )

    is_first_run = False  # with current settings
    if "last_settings" not in st.session_state or st.session_state.last_settings != settings:
        is_first_run = True
        st.session_state.last_settings = settings
        st.session_state.chain = ElectricChain(settings)
        st.session_state.history = [{"time": 0.0, "amperage": 0.0, "voltage": 0.0}]

    sampling_delta = dynamic_sampling_delta(settings)

    if simulate_further or is_first_run:
        for _ in range(POINTS_PER_CHUNK):
            state = st.session_state.chain.step(sampling_delta)
            st.session_state.history.append(asdict(state))

    with st.container(horizontal=True):
        st.line_chart(
            st.session_state.history,
            x="time",
            y="amperage",
            x_label="Time (s)",
            y_label="Amperage (A)",
            color="#ff7f0e",
        )
        st.line_chart(
            st.session_state.history,
            x="time",
            y="voltage",
            x_label="Time (s)",
            y_label="Voltage (V)",
            color="#00bb54",
        )

    st.plotly_chart(
        render_phase_portrait(
            settings=st.session_state.last_settings,
            history=st.session_state.history,
        )
    )
