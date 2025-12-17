from labs.model.vector import Vector3D
from labs.perfect_gas.calculations.calculator import Calculator
from labs.perfect_gas.model.container import Container
from labs.perfect_gas.model.experiment import Experiment
from labs.perfect_gas.model.molecule import Molecule


def test_molecules_stay_in_container() -> None:
    """Test that molecules remain within the container boundaries during simulation."""
    container = Container(length=100.0, width=100.0, height=100.0)
    experiment = Experiment(radius=1.0, number=10, molar_mass=4.0)

    # create molecules that are moving fast towards walls
    molecules = [
        Molecule(
            position=Vector3D(50.0, 50.0, 50.0),
            velocity=Vector3D(1000.0, 0.0, 0.0),  # Towards X+
        ),
        Molecule(
            position=Vector3D(50.0, 50.0, 50.0),
            velocity=Vector3D(-1000.0, 0.0, 0.0),  # Towards X-
        ),
        Molecule(
            position=Vector3D(50.0, 50.0, 50.0),
            velocity=Vector3D(0.0, 1000.0, 0.0),  # Towards Y+
        ),
        Molecule(
            position=Vector3D(50.0, 50.0, 50.0),
            velocity=Vector3D(0.0, 0.0, -1000.0),  # Towards Z-
        ),
    ]

    calculator = Calculator(
        container=container,
        settings=experiment,
        generator=molecules,
        enable_gravity=False,
        enable_internal_collisions=False,
    )

    time_delta = 0.01
    steps = 200

    for _ in range(steps):
        calculator.step(time_delta)

    for molecule in calculator.molecules:
        # Check X bounds
        assert experiment.radius <= molecule.position.x <= container.length - experiment.radius, (
            f"Molecule out of X bounds: {molecule.position.x}"
        )
        # Check Y bounds
        assert experiment.radius <= molecule.position.y <= container.width - experiment.radius, (
            f"Molecule out of Y bounds: {molecule.position.y}"
        )
        # Check Z bounds
        assert experiment.radius <= molecule.position.z <= container.height - experiment.radius, (
            f"Molecule out of Z bounds: {molecule.position.z}"
        )


def test_molecule_count_conserved() -> None:
    """Test that the number of molecules remains constant."""
    container = Container(length=100.0, width=100.0, height=100.0)
    experiment = Experiment(radius=1.0, number=5, molar_mass=4.0)

    molecules = [
        Molecule(
            position=Vector3D(50.0, 50.0, 50.0),
            velocity=Vector3D(10.0, 10.0, 10.0),
        )
        for _ in range(5)
    ]

    calculator = Calculator(
        container=container,
        settings=experiment,
        generator=molecules,
        enable_gravity=False,
        enable_internal_collisions=False,
    )

    initial_count = len(calculator.molecules)
    calculator.step(0.1)
    calculator.step(0.1)

    assert len(calculator.molecules) == initial_count, "Molecule count changed"


def test_zero_velocity_no_movement() -> None:
    """Test that molecules with zero velocity do not move when gravity is off."""
    container = Container(length=100.0, width=100.0, height=100.0)
    experiment = Experiment(radius=1.0, number=1, molar_mass=4.0)

    start_pos = Vector3D(50.0, 50.0, 50.0)
    molecules = [
        Molecule(
            position=Vector3D(50.0, 50.0, 50.0),
            velocity=Vector3D(0.0, 0.0, 0.0),
        )
    ]

    calculator = Calculator(
        container=container,
        settings=experiment,
        generator=molecules,
        enable_gravity=False,
        enable_internal_collisions=False,
    )

    calculator.step(1.0)

    assert calculator.molecules[0].position.x == start_pos.x
    assert calculator.molecules[0].position.y == start_pos.y
    assert calculator.molecules[0].position.z == start_pos.z


def test_directional_pressure_logic() -> None:
    """Test that horizontal movement affects 'sides' pressure and not 'top'/'bottom'."""
    container = Container(length=10.0, width=10.0, height=10.0)
    experiment = Experiment(radius=0.1, number=1, molar_mass=4.0)
    # Molecule moving fast along X axis
    molecules = [Molecule(position=Vector3D(5, 5, 5), velocity=Vector3D(500, 0, 0))]

    calculator = Calculator(
        container=container,
        settings=experiment,
        generator=molecules,
        enable_gravity=False,
        enable_internal_collisions=False,
    )

    # Step enough to hit the wall
    for _ in range(50):
        calculator.step(0.001)

    pressures = calculator.pressures
    assert pressures["sides"] > 0
    assert pressures["top"] == 0
    assert pressures["bottom"] == 0


def test_internal_collisions_logic() -> None:
    """Test that hit_inner_count increments when internal collisions are enabled and occur."""
    container = Container(length=10.0, width=10.0, height=10.0)
    experiment = Experiment(radius=0.5, number=2, molar_mass=4.0)
    # Two molecules moving towards each other
    molecules = [
        Molecule(position=Vector3D(4, 5, 5), velocity=Vector3D(10, 0, 0)),
        Molecule(position=Vector3D(6, 5, 5), velocity=Vector3D(-10, 0, 0)),
    ]

    calculator = Calculator(
        container=container,
        settings=experiment,
        generator=molecules,
        enable_gravity=False,
        enable_internal_collisions=True,
    )

    # Step until they collide (distance 2, relative velocity 20, time ~0.05)
    for _ in range(10):
        calculator.step(0.01)

    assert calculator.hit_inner_count > 0


def test_temperature_velocity_correlation() -> None:
    """Test that higher average molecule speed leads to higher reported temperature."""
    container = Container(length=10.0, width=10.0, height=10.0)
    experiment = Experiment(radius=0.1, number=1, molar_mass=4.0)

    calc_slow = Calculator(
        container=container,
        settings=experiment,
        generator=[Molecule(position=Vector3D(5, 5, 5), velocity=Vector3D(100, 0, 0))],
        enable_gravity=False,
        enable_internal_collisions=False,
    )
    calc_fast = Calculator(
        container=container,
        settings=experiment,
        generator=[Molecule(position=Vector3D(5, 5, 5), velocity=Vector3D(200, 0, 0))],
        enable_gravity=False,
        enable_internal_collisions=False,
    )

    assert calc_fast.temperature > calc_slow.temperature


def test_wall_collision_counter() -> None:
    """Test that hitting a wall increments the hit_with_wall_count."""
    container = Container(length=10.0, width=10.0, height=10.0)
    experiment = Experiment(radius=0.5, number=1, molar_mass=4.0)
    # Starts close to X+ wall, moving towards it
    molecules = [Molecule(position=Vector3D(9.4, 5, 5), velocity=Vector3D(100, 0, 0))]

    calculator = Calculator(
        container=container,
        settings=experiment,
        generator=molecules,
        enable_gravity=False,
        enable_internal_collisions=False,
    )

    calculator.step(0.01)  # 9.4 + 1.0 > 10.0 (radius=0.5, pos=9.4, edge at 9.9)
    assert calculator.hit_with_wall_count > 0
