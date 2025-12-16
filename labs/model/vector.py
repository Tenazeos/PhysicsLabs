from __future__ import annotations

import math
from dataclasses import dataclass
from functools import cached_property

import pandas as pd
import streamlit as st

from labs.util.trigonometry import cos_rounded, sin_rounded


@dataclass
class Vector2D:
    x: float
    y: float

    @classmethod
    def from_polar(cls, norm: float, angle: float) -> Vector2D:
        return Vector2D(norm * cos_rounded(angle), norm * sin_rounded(angle))

    def to_polar(self) -> tuple[float, float]:
        return self.norm, self.angle

    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame({"x": [self.x], "y": [self.y]})

    @cached_property
    def angle(self) -> float:
        return math.atan2(self.y, self.x)

    @cached_property
    def norm(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def __add__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> Vector2D:
        return Vector2D(self.x * other, self.y * other)

    def __matmul__(self, other: Vector2D) -> float:
        return self.x * other.x + self.y * other.y

    def __neg__(self) -> Vector2D:
        return Vector2D(-self.x, -self.y)

    def __truediv__(self, other: float) -> Vector2D:
        return Vector2D(self.x / other, self.y / other)

    def rotate(self, delta_angle: float) -> Vector2D:
        norm, angle = self.to_polar()
        angle += delta_angle
        return Vector2D.from_polar(norm, angle)


def trajectory_to_df(trajectory_data: list[tuple[Vector2D, Vector2D]]) -> pd.DataFrame:
    """
    Build a DataFrame with time, position, and velocity characteristics.

    Columns: time, x, y, velocity, velocity_angle
    """
    return pd.DataFrame(
        [
            {
                "time": index / st.session_state.sampling_steps,
                "x": point.x,
                "y": point.y,
                "velocity_norm": velocity.norm,
                "velocity_angle": math.degrees(velocity.angle),
            }
            for index, (point, velocity) in enumerate(trajectory_data)
        ]
    )


@dataclass
class Vector3D:
    x: float
    y: float
    z: float

    def __add__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Vector3D:
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __neg__(self) -> Vector3D:
        return Vector3D(-self.x, -self.y, -self.z)

    def __truediv__(self, scalar: float) -> Vector3D:
        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar)

    @cached_property
    def norm(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __matmul__(self, other: Vector3D) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z
