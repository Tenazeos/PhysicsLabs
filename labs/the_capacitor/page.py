import math
from enum import StrEnum

import seaborn as sns
import streamlit as st

from labs.model.constant import c

from .calculations import ElectricFieldStrength, calculate_charge, measure_capacity
from .model import DiskCapacitor, DiskPlate, RectCapacitor, RectPlate
from .visualization import disk, rect

CHUNK_SIDE = 0.1  # [cm]

volt_to_statvolt_coef = 1 / (c / 1e6)
statfarad_to_farad_coef = 10e9 / (c**2)


class ShapeMode(StrEnum):
    DISK = "Disk"
    RECTANGLE = "Rectangle"


sns.set_theme(
    style="darkgrid",
    rc={
        "axes.facecolor": "none",
        "figure.facecolor": "none",
        "axes.edgecolor": "white",
        "text.color": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "axes.labelcolor": "white",
        "grid.color": "#444444",
    },
)
sns.set_palette("mako")


def page() -> None:
    st.set_page_config(page_title="The capacitor ⚡️", page_icon="⚡️", layout="wide")

    st.title("The capacitor ⚡️")

    with st.sidebar:
        shape_mode = st.segmented_control(
            "Plate shape",
            options=list(ShapeMode),
            default=ShapeMode.DISK,
            required=True,
            width="stretch",
        )

    if shape_mode == ShapeMode.RECTANGLE:
        rectangle_mode()
    else:
        disk_mode()

    with st.sidebar:
        with st.expander("Constants used"):
            st.html(f"c = {c} m/s")

        with st.expander("Constraints"):
            st.write(
                "The distance between the plates should not exceed the smallest plate side size."
            )


def rectangle_mode() -> None:
    with st.sidebar:
        lower_plate_length = st.slider(
            "Lower plate length (cm)",
            min_value=CHUNK_SIDE * 10,
            max_value=CHUNK_SIDE * 40,
            value=CHUNK_SIDE * 30,
            step=CHUNK_SIDE,
        )
        lower_plate_width = st.slider(
            "Lower plate width (cm)",
            min_value=CHUNK_SIDE * 10,
            max_value=CHUNK_SIDE * 40,
            value=CHUNK_SIDE * 30,
            step=CHUNK_SIDE,
        )
        upper_plate_length = st.slider(
            "Upper plate length (cm)",
            min_value=CHUNK_SIDE * 10,
            max_value=CHUNK_SIDE * 40,
            value=CHUNK_SIDE * 30,
            step=CHUNK_SIDE,
        )
        upper_plate_width = st.slider(
            "Upper plate width (cm)",
            min_value=CHUNK_SIDE * 10,
            max_value=CHUNK_SIDE * 40,
            value=CHUNK_SIDE * 30,
            step=CHUNK_SIDE,
        )

        min_side = min(upper_plate_length, upper_plate_width, lower_plate_length, lower_plate_width)

        distance_min = CHUNK_SIDE * 5 * 10  # [mm]
        distance_max = min_side * 10  # [mm]

        distance = (
            st.slider(
                "Distance between plates (mm)",
                min_value=distance_min,
                max_value=distance_max,
                value=round((distance_min + distance_max) / 2, ndigits=1),
                step=0.1,
            )
            / 10
        )
        voltage = (
            st.slider(
                "Voltage (C)",
                min_value=0.0,
                max_value=100.0,
                value=30.0,
                step=0.1,
            )
            * volt_to_statvolt_coef
        )

    capacitor = RectCapacitor(
        upper_plate=RectPlate(
            length=upper_plate_length,
            width=upper_plate_width,
            chunk_side=CHUNK_SIDE,
        ),
        lower_plate=RectPlate(
            length=lower_plate_length,
            width=lower_plate_width,
            chunk_side=CHUNK_SIDE,
        ),
        distance=distance,
        voltage=voltage,
    )

    charge = calculate_charge(capacitor)
    capacity = measure_capacity(capacitor, charge)
    field = ElectricFieldStrength(capacitor, charge)

    with st.container(horizontal=True, horizontal_alignment="distribute"):
        st.subheader("Rectangle-shaped capacitor")

        st.metric(
            "Capacity",
            (
                f"{capacity * statfarad_to_farad_coef * 10e9:.2f} nF"
                if not math.isnan(capacity)
                else "—"
            ),
            width="content",
        )

    with st.container(horizontal=True, gap="xxsmall"):
        st.plotly_chart(rect.field_volume_3d(capacitor, field))
        st.plotly_chart(rect.plate_slice_slider(capacitor, field))

    st.pyplot(rect.plate_charge(capacitor, charge))


def disk_mode() -> None:
    with st.sidebar:
        upper_plate_radius = st.slider(
            "Upper plate radius (cm)",
            min_value=CHUNK_SIDE * 10,
            max_value=CHUNK_SIDE * 40,
            value=CHUNK_SIDE * 20,
            step=CHUNK_SIDE,
        )
        lower_plate_radius = st.slider(
            "Lower plate radius (cm)",
            min_value=CHUNK_SIDE * 10,
            max_value=CHUNK_SIDE * 40,
            value=CHUNK_SIDE * 20,
            step=CHUNK_SIDE,
        )

        min_radius = min(upper_plate_radius, lower_plate_radius)

        distance_min = CHUNK_SIDE * 5 * 10  # [mm]
        distance_max = min_radius * 2 * 10  # [mm]

        distance = (
            st.slider(
                "Distance between plates (mm)",
                min_value=distance_min,
                max_value=distance_max,
                value=round((distance_min + distance_max) / 2, ndigits=1),
                step=CHUNK_SIDE * 10,
            )
            / 10
        )
        voltage = (
            st.slider(
                "Voltage (V)",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=0.1,
            )
            * volt_to_statvolt_coef
        )

    capacitor = DiskCapacitor(
        upper_plate=DiskPlate(radius=upper_plate_radius, dr=CHUNK_SIDE),
        lower_plate=DiskPlate(radius=lower_plate_radius, dr=CHUNK_SIDE),
        distance=distance,
        voltage=voltage,
    )

    charge = calculate_charge(capacitor)
    capacity = measure_capacity(capacitor, charge)
    field = ElectricFieldStrength(capacitor, charge)

    with st.container(
        horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"
    ):
        st.subheader("Disk-shaped capacitor")

        st.metric(
            "Capacity",
            (
                f"{capacity * statfarad_to_farad_coef * 10e9:.2f} nF"
                if not math.isnan(capacity)
                else "—"
            ),
            width="content",
        )

    with st.container(horizontal=True, gap="xxsmall"):
        st.plotly_chart(disk.field_volume_3d(capacitor, field))
        st.plotly_chart(disk.plate_slice_slider(capacitor, field))

    st.pyplot(disk.plate_charge(capacitor, charge))
