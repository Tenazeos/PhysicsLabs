import math
from collections.abc import Sequence
from functools import partial

import streamlit as st

from labs.model.constant import (
    DAY,
    EARTH_MASS,
    EARTH_ORBIT_RADIUS,
    EARTH_ORBITAL_VELOCITY,
    EARTH_RADIUS,
    HUMAN_EXPIRATION_TIME,
    MARS_MASS,
    MARS_ORBIT_RADIUS,
    MARS_RADIUS,
    MAX_HUMANLY_VIABLE_OVERLOAD,
    RELATIVE_MARS_ORBIT_RADIUS,
    SUN_MASS,
    SUN_RADIUS,
    G,
    g,
)
from labs.model.vector import Vector2D

from .model.flight import FlightEquationType
from .model.planet import Planet
from .model.rocket import Rocket
from .model.stage import FlightStage
from .stage.criteria import is_astronaut_dead
from .stage.planet import flight_equations
from .stage.planet.calculator import RocketFlightCalculator
from .stage.planet.criteria import did_leave_the_planet
from .stage.planet.simulation import simulate_flight
from .stage.space.calculator import RocketInterplanetaryFlightCalculator
from .stage.space.criteria import check_planet_reach
from .stage.space.equation import (
    interplanetary_engine_off_equation,
)
from .stage.space.simulation import simulate_interplanetary_flight
from .visualization.chart import (
    plot_acceleration,
    plot_distance_to_target_chart,
    plot_mass,
    plot_velocity,
    plot_y_position,
)
from .visualization.entity import (
    earth_shape,
    mars_shape,
    orbit_shape,
    rocket_shape,
    sun_shape,
)
from .visualization.render import render_animation


def page() -> None:
    st.set_page_config(page_title="Flight to Mars 🚀", page_icon="🚀", layout="wide")

    with st.sidebar:
        flight_stage: FlightStage | None = st.segmented_control(
            "Flight stage",
            options=list(FlightStage),
            default=FlightStage.EARTH,
            required=True,
        )
        flight_equation_type = FlightEquationType.FIXED_ACCELERATION

        if flight_stage == FlightStage.SPACE:
            show_real_size: bool = st.checkbox("Show real planets size")
            enable_planet_gravity: bool = st.checkbox(
                "Take into account the gravity of both planets", value=True
            )

            relative_rocket_velocity_norm: float = 1000 * st.slider(
                "Relative initial velocity (km/s)",
                min_value=10.0 if enable_planet_gravity else 5.0,
                max_value=20.0,
                value=11.3,
                step=0.01,
            )

            rocket_angle = math.radians(
                st.slider(
                    "Relative start angle, deg",
                    min_value=-90.0,
                    max_value=90.0,
                    value=-18.19,
                    step=0.01,
                )
            )

            earth_position: Vector2D = Vector2D.from_polar(
                EARTH_ORBIT_RADIUS,
                math.radians(
                    st.slider(
                        "Earth position, deg",
                        min_value=-180.0,
                        max_value=180.0,
                        value=-180.0,
                        step=0.1,
                    )
                ),
            )

            st.info("Earth position is set by a radius-vector angle from Sun.")

            def relative_position(v: Vector2D) -> Vector2D:
                return v - earth_position + Vector2D(EARTH_ORBIT_RADIUS, 0)

            relative_rocket_velocity = Vector2D.from_polar(
                relative_rocket_velocity_norm, angle=rocket_angle
            )
            earth_velocity = Vector2D.from_polar(
                EARTH_ORBITAL_VELOCITY, earth_position.angle + math.pi / 2
            )
            rocket_velocity = relative_rocket_velocity + earth_velocity

            with st.expander("Calculated parameters", expanded=True):
                st.markdown(f"Initial velocity: {rocket_velocity.norm / 1000:.02f} km/s")
        else:
            initial_mass: float = 1000 * st.slider(
                "Initial mass, ton",
                min_value=10.0,
                max_value=500.0,
                value=80.0,
                step=0.1,
            )

            fuel_ratio: float = st.slider(
                "Fuel ratio, %",
                min_value=80.0,
                max_value=99.9,
                value=96.0,
                step=0.05,
            )
            fuel_mass: float = initial_mass * fuel_ratio / 100
            netto_mass: float = initial_mass - fuel_mass

            acceleration: float = g * st.slider(
                "Acceleration, g",
                min_value=1.0,
                max_value=10.0,
                value=2.0,
                step=0.05,
                help=(
                    "The rocket engine operates in a mode that maintains constant rocket "
                    "acceleration to protect the astronaut from excessive force."
                ),
            )

            rocket_stream_velocity: float = 1000 * st.slider(
                "Rocket stream velocity, km/s",
                min_value=1.0,
                max_value=7.0,
                value=4.5,
                step=0.02,
            )

            with st.expander("Calculated parameters", expanded=True):
                st.markdown(f"Fuel mass: {fuel_mass / 1000} ton")

        with st.expander("Constants used"):
            st.html(f"G = {G} N·m<sup>2</sup>/kg<sup>2</sup>")

            if flight_stage != FlightStage.MARS:
                st.html(f"Earth mass = {EARTH_MASS:.3e} kg")
                st.html(f"Earth radius = {EARTH_RADIUS:.3e} m")

            if flight_stage == FlightStage.SPACE:
                st.html(f"Sun mass = {SUN_MASS:.3e} kg")
                st.html(f"Sun radius = {SUN_RADIUS:.3e} m")
                st.html(f"Earth orbit radius = {EARTH_ORBIT_RADIUS:.3e} m")
                st.html(f"Mars orbit radius = {MARS_ORBIT_RADIUS:.3e} m")

            if flight_stage != FlightStage.EARTH:
                st.html(f"Mars mass = {MARS_MASS:.3e} kg")
                st.html(f"Mars radius = {MARS_RADIUS:.3e} m")

    st.title("Flight to Mars 🚀")

    match flight_stage:
        case FlightStage.EARTH:
            sampling_delta = 1
            st.session_state.sampling_delta = sampling_delta

            planet = earth_shape(x=0, y=0)
            rocket_shape_at = partial(rocket_shape, size=EARTH_RADIUS / 100)
            initial_rocket = Rocket(
                x=0,
                y=EARTH_RADIUS,
                velocity_x=0,
                velocity_y=0,
                netto_mass=netto_mass,
                fuel_mass=fuel_mass,
                stream_velocity=rocket_stream_velocity,
                acceleration_x=0,
                acceleration_y=acceleration,
            )
            calculator = RocketFlightCalculator(
                rocket=initial_rocket,
                flight_equation=flight_equations[flight_equation_type],
                planet_mass=EARTH_MASS,
            )
            rockets: list[Rocket] = list(simulate_flight(calculator, sampling_delta))

            if not rockets:
                st.rerun()

            figure = render_animation(rockets, rocket_shape_at, [planet])
            st.plotly_chart(figure, key="animation")

            results = st.empty()
            telemetry_charts(rockets, EARTH_MASS, EARTH_RADIUS)

            if is_astronaut_dead(rockets):
                status, warning = results.columns(2)
                warning.warning(
                    "The astronaut is dead. "
                    f"Try not to exceed {MAX_HUMANLY_VIABLE_OVERLOAD}G overload."
                )
            else:
                status = results.empty()

            with status.container():
                if rockets and did_leave_the_planet(rockets[-1], EARTH_MASS):
                    st.success("You have successfully escaped Earth's gravitation!")
                else:
                    st.error("You have not reached the speed to overcome gravitation.")

        case FlightStage.SPACE:
            sampling_delta = 60 * 60 * 4  # 4 hours
            st.session_state.sampling_delta = sampling_delta

            sun_radius = SUN_RADIUS if show_real_size else EARTH_ORBIT_RADIUS / 20
            earth_radius = EARTH_RADIUS if show_real_size else EARTH_ORBIT_RADIUS / 50
            mars_radius = MARS_RADIUS if show_real_size else EARTH_ORBIT_RADIUS / 65

            earth = Planet(x=0, y=0, mass=EARTH_MASS, radius=EARTH_RADIUS)
            mars_position = relative_position(Vector2D(RELATIVE_MARS_ORBIT_RADIUS, 0))
            mars = Planet(x=mars_position.x, y=mars_position.y, mass=MARS_MASS, radius=MARS_RADIUS)
            sun_position = relative_position(Vector2D(-EARTH_ORBIT_RADIUS, 0))
            sun = Planet(x=sun_position.x, y=sun_position.y, mass=SUN_MASS, radius=SUN_RADIUS)

            sun_shape_at = sun_shape(x=sun.x, y=sun.y, radius=sun_radius)
            earth_shape_at = earth_shape(x=earth.x, y=earth.y, radius=earth_radius)
            mars_shape_at = mars_shape(x=mars.x, y=mars.y, radius=mars_radius)

            earth_orbit = orbit_shape(
                center=sun_position,
                semi_major=EARTH_ORBIT_RADIUS,
                semi_minor=EARTH_ORBIT_RADIUS,
            )
            mars_orbit = orbit_shape(
                center=sun_position,
                semi_major=MARS_ORBIT_RADIUS,
                semi_minor=MARS_ORBIT_RADIUS,
            )

            approximate_take_off_height = 2_336_000  # From Earth surface to orbit stage

            rocket_start_point = Vector2D.from_polar(
                EARTH_RADIUS + approximate_take_off_height, angle=rocket_velocity.angle
            )
            rocket_shape_at = partial(rocket_shape, size=earth_radius / 3)

            initial_rocket = Rocket(
                x=rocket_start_point.x,
                y=rocket_start_point.y,
                velocity_x=rocket_velocity.x,
                velocity_y=rocket_velocity.y,
                netto_mass=0,
                fuel_mass=0,
                stream_velocity=0,
                acceleration_x=0,
                acceleration_y=0,
            )

            rockets = list(
                simulate_interplanetary_flight(
                    RocketInterplanetaryFlightCalculator(
                        initial_rocket,
                        interplanetary_engine_off_equation,
                        [earth, mars, sun] if enable_planet_gravity else [sun],
                    ),
                    sampling_delta=sampling_delta,
                    target_planet=mars,
                )
            )

            if not rockets:
                st.rerun()

            figure = render_animation(
                rockets,
                rocket_shape_at,
                [earth_shape_at, mars_shape_at, sun_shape_at],
                [earth_orbit, mars_orbit],
            )
            st.plotly_chart(figure, key="animation")

            status = st.empty()
            with status.container():
                if check_planet_reach(rockets[-2], rockets[-1], mars):
                    st.success("Successfully reached Mars!")
                elif len(rockets) * sampling_delta > HUMAN_EXPIRATION_TIME:
                    st.error(
                        f"The astronaut is dead from hunger. "
                        f"Try not to exceed {HUMAN_EXPIRATION_TIME / DAY} days."
                    )
                else:
                    st.error("You failed to maintain enough speed to reach Mars.")

            st.subheader("Rocket Metrics Over Time")
            col1, col2 = st.columns(2)

            col1.write("**Velocity (km/s)**")
            plot_velocity(col1, rockets[:-1], in_days=True)

            col1.write("**Distance to Target (km)**")
            plot_distance_to_target_chart(col1, rockets, mars, in_days=True)

            col2.write("**Pure Acceleration (g)**")
            plot_acceleration(col2, rockets, in_days=True)

        case FlightStage.MARS:
            sampling_delta = 1
            st.session_state.sampling_delta = sampling_delta

            planet = mars_shape(x=0, y=0)
            rocket_shape_at = partial(rocket_shape, size=MARS_RADIUS / 100)
            initial_rocket = Rocket(
                x=0,
                y=MARS_RADIUS,
                velocity_x=0,
                velocity_y=0,
                netto_mass=netto_mass,
                fuel_mass=1,  # Magic!
                stream_velocity=rocket_stream_velocity * -1,  # A little bit more magic.
                acceleration_x=0,
                acceleration_y=acceleration,
            )

            calculator = RocketFlightCalculator(
                rocket=initial_rocket,
                flight_equation=flight_equations[flight_equation_type],
                planet_mass=MARS_MASS,
            )
            raw_rockets: list[Rocket] = list(simulate_flight(calculator, sampling_delta))
            rockets: list[Rocket] = list(filter(lambda r: r.mass <= initial_mass, raw_rockets))

            if not rockets:
                st.rerun()

            figure = render_animation(rockets[::-1], rocket_shape_at, [planet])
            st.plotly_chart(figure, key="animation")

            results = st.empty()
            if did_leave_the_planet(rockets[-1], MARS_MASS):
                telemetry_charts(rockets[::-1], MARS_MASS, MARS_RADIUS)

            if is_astronaut_dead(rockets):
                status, warning = results.columns(2)
                warning.warning(
                    f"The astronaut is dead. "
                    f"Try not to exceed {MAX_HUMANLY_VIABLE_OVERLOAD}G overload."
                )
            else:
                status = results.empty()

            with status.container():
                if rockets and did_leave_the_planet(rockets[-1], MARS_MASS):
                    st.success(
                        f"You have to turn on engine at "
                        f"{(rockets[-1].y - MARS_RADIUS) / 1000:.01f}km above to successfully land "
                        f"on Mars. You should have only "
                        f"{rockets[-1].fuel_mass / fuel_mass * 100:.02f}% "
                        f"({rockets[-1].fuel_mass:.02f} ton) of a fuel tank to be full."
                    )
                else:
                    st.error(
                        f"You probably have been smashed into pieces. You must have "
                        f"{(raw_rockets[-1].fuel_mass / fuel_mass - 1) * 100:.02f}% "
                        f"more fuel ({rockets[-1].fuel_mass:.02f} ton in total) "
                        f"while maintaining the same payload mass."
                    )

        case None:
            st.warning("Choose one of the stages to simulate.")


def telemetry_charts(rockets: Sequence[Rocket], planet_mass: float, planet_radius: float) -> None:
    st.subheader("Rocket Metrics Over Time")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Velocity (km/s)**")
        velocity_chart = st.empty()
        st.write("**Mass (ton)**")
        mass_chart = st.empty()
    with col2:
        st.write("**Y Position (km)**")
        y_chart = st.empty()
        st.write("**Acceleration (g)**")
        acceleration_chart = st.empty()

    plot_velocity(velocity_chart, rockets, planet_mass)
    plot_mass(mass_chart, rockets)
    plot_y_position(y_chart, rockets, planet_radius)
    plot_acceleration(acceleration_chart, rockets)
