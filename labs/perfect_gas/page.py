import plotly.express as px
import streamlit as st

from .calculations import Calculator, create_all_molecules_at_the_bottom
from .model.container import Container


def page() -> None:
    st.title("Perfect Gas [DEBUG]")

    st.sidebar.header("Параметры контейнера")
    radius = st.sidebar.slider("Радиус молекул", 1.0, 10.0, 5.0)
    height = st.sidebar.slider("Высота", 100.0, 500.0, 200.0)
    width = st.sidebar.slider("Ширина", 100.0, 500.0, 200.0)

    st.sidebar.header("Параметры молекул")
    n_molecules = st.sidebar.slider("Количество молекул", 20, 1000, 50)
    max_velocity = st.sidebar.slider("Макс. скорость", 10.0, 100.0, 30.0)

    st.sidebar.header("Симуляция")
    steps = st.sidebar.slider("Количество шагов", 10, 1000, 200)
    time_delta = st.sidebar.slider("Временной шаг (dt)", 0.01, 0.1, 0.05)
    run_simulation = st.sidebar.button("Запустить симуляцию")

    container = Container(height=height, width=width)

    calculator: Calculator = Calculator(
        molecules_gen=create_all_molecules_at_the_bottom(
            container=container,
            count=n_molecules,
            max_velocity=max_velocity,
        ),
        container=container,
        molecules_radius=radius,
    )

    if run_simulation:
        progress_bar = st.progress(0)
        status_text = st.empty()

        for step in range(steps):
            calculator.step(time_delta)

            progress = (step + 1) / steps
            progress_bar.progress(progress)
            status_text.text(f"Шаг {step + 1}/{steps}")

        velocities_after = [m.velocity.norm for m in calculator.molecules]

        st.subheader("Распределение модулей скоростей")
        fig = px.histogram(
            x=velocities_after,
            title=f"Скорости молекул (после {steps} шагов)",
            labels={"x": "Модуль скорости", "y": "Количество молекул"},
        )
        fig.update_layout(showlegend=False, bargap=0.1)
        st.plotly_chart(fig)
