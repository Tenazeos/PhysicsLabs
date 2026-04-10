from dataclasses import dataclass


@dataclass(slots=True)
class State:
    voltage: float
    amperage: float
