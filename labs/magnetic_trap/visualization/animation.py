from collections.abc import Sequence

import numpy as np
import plotly.graph_objects as go

from labs.magnetic_trap.models import MagneticTrap, SegmentedRing, State


def render_particle_animation(
    trap: MagneticTrap,
    initial_velocity: np.ndarray,
    states: Sequence[State],
    frame_duration: int = 5,
) -> go.Figure:
    positions = np.array([s.position for s in states])
    positions_x, positions_y, positions_z = positions[:, 0], positions[:, 1], positions[:, 2]

    def get_ring_coords(ring: SegmentedRing) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        points = ring.points
        points = np.vstack([points, points[0]])
        return points[:, 0], points[:, 1], points[:, 2]

    upper_x, upper_y, upper_z = get_ring_coords(trap.upper_ring)
    lower_x, lower_y, lower_z = get_ring_coords(trap.lower_ring)

    max_radius = (
        max(
            trap.upper_ring.radius,
            trap.lower_ring.radius,
            np.max(np.abs(positions_x)),
            np.max(np.abs(positions_y)),
        )
        * 1.1
    )

    min_z = float(min(trap.lower_ring.z_cord, np.min(positions_z)))
    max_z = float(max(trap.upper_ring.z_cord, np.max(positions_z)))
    z_padding = float(max(0.1, (max_z - min_z) * 0.1))

    trace_upper = go.Scatter3d(
        x=upper_x,
        y=upper_y,
        z=upper_z,
        mode="lines",
        line={"color": "#1f77b4", "width": 5},
        name="Upper Ring",
    )
    trace_lower = go.Scatter3d(
        x=lower_x,
        y=lower_y,
        z=lower_z,
        mode="lines",
        line={"color": "#1f77b4", "width": 5},
        name="Lower Ring",
    )

    trace_z_axis = go.Scatter3d(
        x=[0, 0],
        y=[0, 0],
        z=[min_z - z_padding, max_z + z_padding],
        mode="lines",
        line={"color": "gray", "width": 2, "dash": "dash"},
        name="Z-Axis",
    )

    trace_trajectory = go.Scatter3d(
        x=positions_x,
        y=positions_y,
        z=positions_z,
        mode="lines",
        line={"color": "#ff7f0e", "width": 3},
        opacity=0.4,
        name="Trajectory",
    )

    velocity_normalized = initial_velocity / np.linalg.norm(initial_velocity)

    arrow_length = float(max_radius * 0.15)
    head_length = arrow_length * 0.2
    stem_length = arrow_length - head_length

    stem_end = (
        np.array([positions_x[0], positions_y[0], positions_z[0]])
        + velocity_normalized * stem_length
    )

    trace_velocity_stem = go.Scatter3d(
        x=[positions_x[0], stem_end[0]],
        y=[positions_y[0], stem_end[1]],
        z=[positions_z[0], stem_end[2]],
        mode="lines",
        line={"color": "#00bb54", "width": 1.5},
        name="Velocity Stem",
    )

    trace_velocity_head = go.Cone(
        x=[stem_end[0]],
        y=[stem_end[1]],
        z=[stem_end[2]],
        u=[velocity_normalized[0]],
        v=[velocity_normalized[1]],
        w=[velocity_normalized[2]],
        colorscale=[[0, "#00bb54"], [1, "#00bb54"]],
        showscale=False,
        sizemode="absolute",
        sizeref=head_length,
        anchor="tail",
        name="Velocity Head",
    )

    trace_particle = go.Scatter3d(
        x=[positions_x[0]],
        y=[positions_y[0]],
        z=[positions_z[0]],
        mode="markers",
        marker={"color": "#ff7f0e", "size": 3},
        name="Particle",
    )

    frames = []
    for i in range(1, len(states)):
        frame = go.Frame(
            data=[
                go.Scatter3d(x=[positions_x[i]], y=[positions_y[i]], z=[positions_z[i]]),
            ],
            name=str(i),
            traces=[6],
        )
        frames.append(frame)

    layout = go.Layout(
        scene={
            "xaxis": {"range": [-max_radius, max_radius], "autorange": False},
            "yaxis": {"range": [-max_radius, max_radius], "autorange": False},
            "zaxis": {"range": [min_z - z_padding, max_z + z_padding], "autorange": False},
            "aspectmode": "cube",
        },
        height=800,
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "y": 0.9,
                "x": 0.1,
                "xanchor": "left",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": frame_duration, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 0},
                            },
                        ],
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [
                            [None],
                            {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"},
                        ],
                    },
                ],
            }
        ],
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
        showlegend=False,
    )

    return go.Figure(
        data=[
            trace_upper,
            trace_lower,
            trace_z_axis,
            trace_trajectory,
            trace_velocity_stem,
            trace_velocity_head,
            trace_particle,
        ],
        layout=layout,
        frames=frames,
    )
