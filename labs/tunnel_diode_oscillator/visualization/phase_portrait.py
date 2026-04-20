import numpy as np
import plotly.graph_objects as go

from ..model import Settings


def render_phase_portrait(settings: Settings, history: list[dict[str, float]]) -> go.Figure:
    voltage_history = [state["voltage"] for state in history]
    amperage_history = [state["amperage"] for state in history]

    voltage_values = np.linspace(0.0, 2.5, 300)
    amperage_values = [settings.diode.amperage(v) for v in voltage_values]

    amperage_load = [
        (settings.electromotive_force - v) / settings.resistance for v in voltage_values
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=voltage_values,
            y=amperage_values,
            mode="lines",
            name="Diode I-V curve",
            line={"color": "#1f77b4", "width": 3},
        )
    )

    fig.add_trace(
        go.Scatter(
            x=voltage_values,
            y=amperage_load,
            mode="lines",
            name="Load line",
            line={"color": "#dc143c", "width": 2, "dash": "dash"},
        )
    )

    fig.add_trace(
        go.Scatter(
            x=voltage_history,
            y=amperage_history,
            mode="lines",
            name="Trajectory",
            line={"color": "#ff7f0e", "width": 2, "shape": "spline"},
            opacity=0.3,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[voltage_history[-1]],
            y=[amperage_history[-1]],
            mode="markers",
            name="Latest state",
            marker={"color": "#ff7f0e", "size": 12, "line": {"color": "white", "width": 2}},
        )
    )

    fig.update_layout(
        title="Phase Space",
        xaxis_title="Voltage (V)",
        yaxis_title="Amperage (A)",
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
        xaxis={"range": [0, 2.5], "showgrid": True, "gridcolor": "#333333"},
        yaxis={"range": [-0.002, 0.015], "showgrid": True, "gridcolor": "#333333"},
        margin={"l": 40, "r": 40, "t": 40, "b": 40},
        legend={"x": 0.02, "y": 0.98, "bgcolor": "rgba(0,0,0,0.5)"},
    )

    return fig
