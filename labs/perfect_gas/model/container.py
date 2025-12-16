from dataclasses import dataclass


@dataclass(frozen=True)
class Container:
    length: float
    height: float
    width: float
