from typing import Literal

from labs.model.vector import Vector3D

type SurfacePosition = Literal["x+", "x-", "y+", "y-", "z+", "z-"]

# Surface normal vector points INSIDE the container
surface_norm_by_position = {
    "x+": Vector3D(-1, 0, 0),
    "x-": Vector3D(1, 0, 0),
    "y+": Vector3D(0, -1, 0),
    "y-": Vector3D(0, 1, 0),
    "z+": Vector3D(0, 0, -1),
    "z-": Vector3D(0, 0, 1),
}
