from dataclasses import dataclass


@dataclass(slots=True)
class State:
    time: float
    amperage: float
    voltage: float
