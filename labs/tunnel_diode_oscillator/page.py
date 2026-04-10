import streamlit as st

from .calculations import ElectricChain
from .model import Settings, State, TunnelDiode


def page() -> None:
    st.set_page_config(page_title="Tunnel diode oscillator 🔃", page_icon="🔃", layout="wide")

    st.title("Tunnel diode oscillator 🔃")

    # settings = Settings(
    #     resistance=st.sidebar.slider("Resistance", 0.1, 1.0, 0.1),
    #     capacity=st.sidebar.slider("Capacity", 0.1, 1.0, 0.1),
    #     inductance=st.sidebar.slider("Inductance", 0.1, 1.0, 0.1),
    #     electromotive_force=st.sidebar.slider("Electromotive_force", 0.1, 1.0, 0.1),
    #     diode=TunnelDiode()
    # )

    settings = Settings(
        resistance=0.5, capacity=1e-8, inductance=1e-5, electromotive_force=1, diode=TunnelDiode()
    )

    if st.sidebar.button("Calculate"):
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

        chain = ElectricChain(settings)

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
