# ruff: noqa: RUF001
import streamlit as st
from plotly import express as px

from .calculations import Calculator, random_place
from .model import Experiment
from .model.container import Container


def page() -> None:
    st.title("Perfect Gas")

    st.sidebar.header("Параметры сосуда")
    # 1e3 - conversation from centimetre to nanometre
    container = Container(
        length=st.sidebar.slider("Длина, микрометры", 0.1, 10.0, 1.0) * 1e3,
        width=st.sidebar.slider("Ширина, микрометры", 0.1, 10.0, 1.0) * 1e3,
        height=st.sidebar.slider("Высота, микрометры", 0.1, 10.0, 1.0) * 1e3,
    )

    st.sidebar.header("Параметры эксперимента")
    experiment = Experiment(
        radius=st.sidebar.slider("Радиус молекул, нм", 0.1, 10.0, 2.0),
        number=st.sidebar.slider("Количество молекул, штук", 500, 5000, 1000),
        molar_mass=st.sidebar.slider("Молярная масса, г/моль", 1.0, 10.0, 4.0),
    )

    max_velocity = st.sidebar.slider(
        "Максимальная стартовая скорость(по направлению), м/с", 100.0, 1000.0, 200.0
    )
    min_velocity = st.sidebar.slider(
        "Минимальная стартовая скорость(по направлению), м/с", 100.0, 1000.0, 200.0
    )
    enable_gravity = st.sidebar.checkbox("Включить гравитацию")

    steps = st.sidebar.slider("Число шагов", 10, 1000, 100)

    time_delta = 2 * experiment.radius / max_velocity  # in nanoseconds

    run_simulation = st.sidebar.button("Запустить симуляцию")

    calculator: Calculator = Calculator(
        container=container,
        settings=experiment,
        generator=random_place(min_velocity, max_velocity, experiment.number, container),
        enable_gravity=enable_gravity,
    )

    if run_simulation:
        st.write(
            f"Optimal time delta: {time_delta} nanoseconds, "
            f"total time: {time_delta * steps} nanoseconds."
        )

        start_vel = [m.velocity.norm for m in calculator.molecules]

        progress_bar = st.progress(0)
        status_text = st.empty()

        for step in range(steps):
            calculator.step(time_delta)
            progress_bar.progress((step + 1) / steps)
            status_text.text(f"Шаг: {step + 1}/{steps}")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Температура, мили Кельвины",
                value=calculator.temperature,
            )

            st.metric(
                label="Давление, мили Паскали",
                value=calculator.pressure,
            )

        with col2:
            st.metric(label="Количество внутренних столкновений", value=calculator.hit_inner_count)
            st.metric(
                label="Количество столкновений со стеной", value=calculator.hit_with_wall_count
            )

        col1, col2 = st.columns(2)

        with col1:
            fig = px.histogram(
                x=start_vel,
                title="Начальное распределение модулей скоростей",
                labels={"x": "Модуль скорости, м/с", "y": "Количество молекул"},
            )
            fig.update_layout(showlegend=False, bargap=0.1)

            st.plotly_chart(fig)

        with col2:
            fig = px.histogram(
                x=[m.velocity.norm for m in calculator.molecules],
                title="Конечное распределение модулей скоростей",
                labels={"x": "Модуль скорости, м/с", "y": "Количество молекул"},
            )
            fig.update_layout(showlegend=False, bargap=0.1)

            st.plotly_chart(fig)
