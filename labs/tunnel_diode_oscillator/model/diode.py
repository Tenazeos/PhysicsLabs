from abc import ABC, abstractmethod


class Diode(ABC):
    @abstractmethod
    def amperage(self, voltage: float) -> float: ...


class TunnelDiode(Diode):
    a: float = 4 * 1e-3
    b: float = -16 * 1e-3
    c: float = 17 * 1e-3

    def amperage(self, voltage: float) -> float:
        return (self.a * voltage**3 + self.b * voltage**2 + self.c * voltage) if voltage > 0 else 0
