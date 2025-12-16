# ruff: noqa: RUF001
import streamlit as st
from plotly import express as px

from .calculations import Calculator, random_place
from .model import Experiment
from .model.container import Container


def page() -> None:
    st.title("Perfect Gas")

    st.sidebar.header("Параметры сосуда")
    # 1e7 - conversation from centimetre to nanometre
    container = Container(
        length=st.sidebar.slider("Длина, см", 1.0, 100.0, 5.0) * 1e7,
        width=st.sidebar.slider("Ширина, см", 1.0, 100.0, 5.0) * 1e7,
        height=st.sidebar.slider("Высота, см", 1.0, 100.0, 5.0) * 1e7,
    )

    st.sidebar.header("Параметры эксперимента")
    experiment = Experiment(
        radius=st.sidebar.slider("Радиус молекул, нм", 0.1, 10.0, 2.0),
        number=st.sidebar.slider("Количество молекул, штук", 1000, 5000, 2000),
        molar_mass=st.sidebar.slider("Молярная масса, г/моль", 1.0, 10.0, 4.0),
    )

    max_velocity = st.sidebar.slider(
        "Максимальная стартовая скорость(по направлению), м/с", 10.0, 200.0, 50.0
    )
    min_velocity = st.sidebar.slider(
        "Минимальная стартовая скорость(по направлению), м/с", 10.0, 200.0, 10.0
    )
    enable_gravity = st.sidebar.checkbox("Включить гравитацию")

    total_time = st.sidebar.slider("Время симуляции, наносекунды", 0.01, 1.0, 0.1)

    time_delta = 2 * experiment.radius / max_velocity  # in nanoseconds

    run_simulation = st.sidebar.button("Запустить симуляцию")

    calculator: Calculator = Calculator(
        container=container,
        settings=experiment,
        generator=random_place(min_velocity, max_velocity, experiment.number, container),
        enable_gravity=enable_gravity,
    )

    if run_simulation:
        st.write(f"Optimal time delta: {time_delta} nanoseconds")
        progress_bar = st.progress(0)
        status_text = st.empty()

        col1, col2 = st.columns(2)
        with col1:
            temp = st.empty()
        with col2:
            pres = st.empty()

        chart = st.empty()

        current_time = 0
        while current_time < total_time:
            calculator.step(time_delta)

            state = calculator.get_state()

            temp.metric(
                label="Температура, мили Кельвины",
                value=state.temperature,
            )

            pres.metric(
                label="Давление, мили Паскали",
                value=state.pressure,
            )

            progress_bar.progress(current_time / total_time)
            status_text.text(f"Время: {current_time}")

            fig = px.histogram(
                x=[m.velocity.norm for m in calculator.molecules],
                title="Распределение модулей скоростей",
                labels={"x": "Модуль скорости, м/с", "y": "Количество молекул"},
            )
            fig.update_layout(showlegend=False, bargap=0.1)

            chart.plotly_chart(fig, key=str(current_time))

            current_time += time_delta
