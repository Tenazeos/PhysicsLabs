import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import seaborn as sns
from matplotlib import pyplot as plt

from ..calculations import ElectricFieldStrength
from ..model import RectCapacitor
from .util import get_raw_slice_data


def field_volume_3d(capacitor: RectCapacitor, field: ElectricFieldStrength) -> go.Figure:
    x_flat, y_flat, z_flat = [], [], []
    u_flat, v_flat, w_flat = [], [], []

    grid_coords = capacitor.covering_chunks_at_zero_height
    x_base = grid_coords[:, 1]
    y_base = grid_coords[:, 0]

    lower_x_min, lower_x_max = 0, capacitor.lower_plate.width
    lower_y_min, lower_y_max = 0, capacitor.lower_plate.length
    lower_plate_x = [lower_x_min, lower_x_max, lower_x_max, lower_x_min, lower_x_min]
    lower_plate_y = [lower_y_min, lower_y_min, lower_y_max, lower_y_max, lower_y_min]

    upper_x_min, upper_x_max = 0, capacitor.upper_plate.width
    upper_y_min, upper_y_max = 0, capacitor.upper_plate.length
    upper_plate_x = [upper_x_min, upper_x_max, upper_x_max, upper_x_min, upper_x_min]
    upper_plate_y = [upper_y_min, upper_y_min, upper_y_max, upper_y_max, upper_y_min]

    steps = np.arange(1 / 8, 1.0, 1 / 8)

    for coef in steps:
        z_val = capacitor.distance * coef
        z_base = np.full_like(x_base, z_val)

        u, v, w = get_raw_slice_data(capacitor, field, grid_coords, coef)

        mag_3d = np.sqrt(u**2 + v**2 + w**2)

        valid = mag_3d > 1e-10

        compressed_mag = np.zeros_like(mag_3d)
        compressed_mag[valid] = mag_3d[valid] ** 0.25

        u_plot = np.zeros_like(u)
        v_plot = np.zeros_like(v)
        w_plot = np.zeros_like(w)

        u_plot[valid] = (u[valid] / mag_3d[valid]) * compressed_mag[valid]
        v_plot[valid] = (v[valid] / mag_3d[valid]) * compressed_mag[valid]
        w_plot[valid] = (w[valid] / mag_3d[valid]) * compressed_mag[valid]

        stride = 2

        x_flat.extend(x_base[::stride])
        y_flat.extend(y_base[::stride])
        z_flat.extend(z_base[::stride])

        u_flat.extend(u_plot[::stride])
        v_flat.extend(v_plot[::stride])
        w_flat.extend(w_plot[::stride])

    # noinspection PyUnboundLocalVariable
    cone_trace = go.Cone(
        x=x_flat,
        y=y_flat,
        z=z_flat,
        u=u_flat,
        v=v_flat,
        w=w_flat,
        colorscale="Plasma",
        sizemode="scaled",
        sizeref=np.max(compressed_mag) * 2 if len(compressed_mag) > 0 else 0.1,
        showscale=True,
        colorbar={"title": "Intensity (power scaled)"},
    )

    lower_plate_trace = go.Scatter3d(
        x=lower_plate_x,
        y=lower_plate_y,
        z=[0] * 5,
        mode="lines",
        line={"color": "lime", "width": 4},
        hoverinfo="skip",
        showlegend=False,
    )

    upper_plate_trace = go.Scatter3d(
        x=upper_plate_x,
        y=upper_plate_y,
        z=[capacitor.distance] * 5,
        mode="lines",
        line={"color": "lime", "width": 4},
        hoverinfo="skip",
        showlegend=False,
    )

    fig = go.Figure(data=[cone_trace, lower_plate_trace, upper_plate_trace])

    fig.update_layout(
        template="plotly_dark",
        title="Interactive electric field in 3D",
        margin={"l": 0, "r": 0, "t": 40, "b": 0},
        scene={
            "aspectmode": "data",
            "camera": {"eye": {"x": 1.5, "y": 1.5, "z": 1.2}},
        },
    )

    return fig


def plate_slice_slider(capacitor: RectCapacitor, field: ElectricFieldStrength) -> go.Figure:
    grid_coords = capacitor.covering_chunks_at_zero_height
    y = grid_coords[:, 0]
    x = grid_coords[:, 1]
    height_coefs = np.array([i / 8 for i in range(1, 8)])

    u0, v0, _ = get_raw_slice_data(capacitor, field, grid_coords, height_coefs[0])
    global_max_mag = np.max(np.hypot(u0, v0)) * 0.5

    fig = go.Figure()
    frames = []
    slider_steps = []

    for i, coef in enumerate(height_coefs):
        u, v, _ = get_raw_slice_data(capacitor, field, grid_coords, coef)

        magnitude = np.hypot(u, v)
        max_mag_local = np.max(magnitude)

        valid = magnitude > (max_mag_local * 1e-10)
        u_norm = np.zeros_like(u)
        v_norm = np.zeros_like(v)
        u_norm[valid] = u[valid] / magnitude[valid]
        v_norm[valid] = v[valid] / magnitude[valid]

        heatmap_trace = go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker={
                "size": 14,
                "symbol": "square",
                "color": magnitude,
                "colorscale": "Plasma",
                "cmin": 0,
                "cmax": global_max_mag,
                "colorbar": {"title": "Intensity (V/m)"} if i == 0 else None,
            },
            name="Magnitude",
            hoverinfo="skip",
        )

        stride = 2

        quiver_fig = ff.create_quiver(
            x[::stride],
            y[::stride],
            u_norm[::stride],
            v_norm[::stride],
            scale=0.08,
            arrow_scale=0.3,
            line={"color": "white", "width": 1},
        )
        quiver_trace = quiver_fig.data[0]

        frame_name = f"slice_{i}"
        frames.append(go.Frame(data=[heatmap_trace, quiver_trace], name=frame_name))

        if i == 0:
            fig.add_trace(heatmap_trace)
            fig.add_trace(quiver_trace)

        slider_steps.append(
            {
                "method": "animate",
                "args": [
                    [frame_name],
                    {
                        "mode": "immediate",
                        "frame": {"duration": 300, "redraw": True},
                        "transition": {"duration": 0.1},
                    },
                ],
                "label": f"{coef:.3f}d",
            }
        )

    fig.frames = frames
    fig.update_layout(
        template="plotly_dark",
        title="Interactive electric field slice",
        xaxis={"scaleanchor": "y", "scaleratio": 1, "visible": False},
        yaxis={"visible": False},
        height=550,
        showlegend=False,
        margin={"l": 0, "r": 0, "t": 40, "b": 0},
        sliders=[
            {
                "active": 0,
                "currentvalue": {"prefix": "Height (z/d): "},
                "pad": {"t": 50},
                "steps": slider_steps,
            }
        ],
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [
                            None,
                            {"frame": {"duration": 300, "redraw": True}, "fromcurrent": True},
                        ],
                    }
                ],
            }
        ],
    )

    return fig


def plate_charge(capacitor: RectCapacitor, charge: np.ndarray) -> plt.Figure:
    fig, (ax_lower, ax_upper) = plt.subplots(1, 2, figsize=(16, 6))

    x_step_lower = max(1, capacitor.lower_plate.length_chunk_count // 10)
    y_step_lower = max(1, capacitor.lower_plate.width_chunk_count // 10)

    lower_data = charge[: capacitor.lower_plate.chunk_count]
    sns.heatmap(
        lower_data.reshape(
            capacitor.lower_plate.length_chunk_count, capacitor.lower_plate.width_chunk_count
        ),
        square=True,
        xticklabels=x_step_lower,
        yticklabels=y_step_lower,
        cmap="plasma",
        ax=ax_lower,
    )
    ax_lower.set_title("Lower Plate Charge")
    ax_lower.tick_params(axis="x", rotation=0)
    ax_lower.tick_params(axis="y", rotation=0)

    x_step_upper = max(1, capacitor.upper_plate.length_chunk_count // 10)
    y_step_upper = max(1, capacitor.upper_plate.width_chunk_count // 10)

    upper_data = charge[capacitor.lower_plate.chunk_count :]
    sns.heatmap(
        upper_data.reshape(
            capacitor.upper_plate.length_chunk_count, capacitor.upper_plate.width_chunk_count
        ),
        square=True,
        xticklabels=x_step_upper,
        yticklabels=y_step_upper,
        cmap="plasma",
        ax=ax_upper,
    )
    ax_upper.set_title("Upper Plate Charge")
    ax_upper.tick_params(axis="x", rotation=0)
    ax_upper.tick_params(axis="y", rotation=0)

    return fig
