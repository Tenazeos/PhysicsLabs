from dataclasses import dataclass


@dataclass
class Screen:
    z_position: float
    width: float
    height: float


@dataclass
class Settings:
    screen: Screen
    distance_between_slits: float
    wavelength: float
