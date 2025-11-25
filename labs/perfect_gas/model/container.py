from dataclasses import dataclass


@dataclass(frozen=True)
class Container:
    height: float
    width: float
