from dataclasses import dataclass


@dataclass(frozen=True)
class Experiment:
    """
    Storage for base experiment settings

    radius - effective radius of the molecule, in nanometers
    number - number of molecules
    molar_mass - molar mass, in g/mole
    """

    radius: float
    number: int
    molar_mass: float
