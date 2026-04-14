# ruff: noqa: RUF001
from dataclasses import dataclass
from enum import Enum

import streamlit as st

from labs.util.formatting import superscript_digits

from .calculations import ElectricChain
from .model import Settings, State, TunnelDiode

type ScientificPair = tuple[float, int]  # float * 10^(int)


@dataclass
class ParameterPresetData:
    resistance: ScientificPair
    capacity: ScientificPair
    inductance: ScientificPair
    electromotive_force: ScientificPair


class ParameterPreset(Enum):
    SINUS = ParameterPresetData(
        resistance=(5.0, -1),
        capacity=(1.0, -8),
        inductance=(1.0, -5),
        electromotive_force=(1.0, 0),
    )


def page() -> None:
    st.set_page_config(page_title="Tunnel diode oscillator 🔃", page_icon="🔃", layout="wide")

    st.title("Tunnel diode oscillator 🔃")

    with st.sidebar:
        preset: ParameterPreset = st.segmented_control(
            "Parameter preset",
            options=list(ParameterPreset),
            default=ParameterPreset.SINUS,
            format_func=lambda preset: preset.name.replace("_", " ").capitalize(),
            required=True,
            width="stretch",
        )

        with st.container(horizontal=True, horizontal_alignment="distribute"):
            resistance = st.slider(
                "Resistance (Ω)",
                min_value=0.01,
                max_value=10.0,
                step=0.01,
                value=preset.value.resistance[0],
            ) * 10 ** st.selectbox(
                "<power>",
                options=range(-3, 4),
                index=range(-3, 4).index(preset.value.resistance[1]),
                format_func=lambda exp: f"×10{str(exp).translate(superscript_digits)}",
                label_visibility="hidden",
                width=100,
            )

        with st.container(horizontal=True, horizontal_alignment="distribute"):
            capacity = st.slider(
                "Capacity (F)",
                min_value=0.01,
                max_value=10.0,
                step=0.01,
                value=preset.value.capacity[0],
            ) * 10 ** st.selectbox(
                "<power>",
                options=range(-10, -5),
                index=range(-10, -5).index(preset.value.capacity[1]),
                format_func=lambda exp: f"×10{str(exp).translate(superscript_digits)}",
                label_visibility="hidden",
                width=100,
            )

        with st.container(horizontal=True, horizontal_alignment="distribute"):
            inductance = st.slider(
                "Inductance (H)",
                min_value=0.01,
                max_value=10.0,
                step=0.01,
                value=preset.value.inductance[0],
            ) * 10 ** st.selectbox(
                "<power>",
                options=range(-7, -2),
                index=range(-7, -2).index(preset.value.inductance[1]),
                format_func=lambda exp: f"×10{str(exp).translate(superscript_digits)}",
                label_visibility="hidden",
                width=100,
            )

        with st.container(horizontal=True, horizontal_alignment="distribute"):
            electromotive_force = st.slider(
                "Electromotive force (V)",
                min_value=0.01,
                max_value=10.0,
                step=0.01,
                value=preset.value.electromotive_force[0],
            ) * 10 ** st.selectbox(
                "<power>",
                options=range(-3, 4),
                index=range(-3, 4).index(preset.value.electromotive_force[1]),
                format_func=lambda exp: f"×10{str(exp).translate(superscript_digits)}",
                label_visibility="hidden",
                width=100,
            )

    settings = Settings(
        resistance=resistance,
        capacity=capacity,
        inductance=inductance,
        electromotive_force=electromotive_force,
        diode=TunnelDiode(),
    )
    chain = ElectricChain(settings)

    amper_chart = st.line_chart(
        [
            {
                "I": 0.0,
                "t": 0.0,
            }
        ],
        x="t",
        y="I",
    )
    volt_chart = st.line_chart(
        [
            {
                "U": 0.0,
                "t": 0.0,
            }
        ],
        x="t",
        y="U",
    )

    current_time = 0.0
    for _i in range(20):
        state: State = chain.step(0.1)
        current_time += 0.1

        amper_chart.add_rows(
            [
                {
                    "I": state.amperage,
                    "t": current_time,
                }
            ]
        )

        volt_chart.add_rows(
            [
                {
                    "U": state.voltage,
                    "t": current_time,
                }
            ]
        )
