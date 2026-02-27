import streamlit as st

from labs.model.constant import c

from .model import RectCapacitor, RectPlate

volt_to_statvolt_coef = 1 / (c / 1e6)


def page() -> None:
    st.set_page_config(page_title="The capacitor ⚡️", page_icon="⚡️", layout="wide")

    st.title("The capacitor ⚡️")

    with st.sidebar:
        chunk_side = (
            st.slider(
                "Chunk side (mm)",
                min_value=0.01,
                max_value=1.0,
                value=0.1,
                step=0.01,
            )
            / 10
        )

        upper_plate_length = st.slider(
            "Upper plate length (cm)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=chunk_side,
        )
        upper_plate_width = st.slider(
            "Upper plate width (cm)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=chunk_side,
        )
        lower_plate_length = st.slider(
            "Lower plate length (cm)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=chunk_side,
        )
        lower_plate_width = st.slider(
            "Lower plate width (cm)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=chunk_side,
        )

        distance = (
            st.slider(
                "Distance between plates (mm)",
                min_value=0.1,
                max_value=10.0,
                value=1.0,
                step=0.1,
            )
            / 10
        )
        voltage = (
            st.slider(
                "Voltage (V)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
            )
            * volt_to_statvolt_coef
        )

        st.session_state.capacitor = RectCapacitor(
            upper_plate=RectPlate(
                length=upper_plate_length,
                width=upper_plate_width,
                chunk_side=chunk_side,
            ),
            lower_plate=RectPlate(
                length=lower_plate_length,
                width=lower_plate_width,
                chunk_side=chunk_side,
            ),
            distance=distance,
            voltage=voltage,
        )

    st.subheader("Here will be some content... eventually :)")
