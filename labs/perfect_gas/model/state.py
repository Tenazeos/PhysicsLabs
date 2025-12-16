from dataclasses import dataclass


@dataclass(slots=True)
class SystemState:
    temperature: float
    pressure: float
