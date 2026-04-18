from dataclasses import dataclass


@dataclass(slots=True)
class State:
    time: float
    voltage: float
    amperage: float
