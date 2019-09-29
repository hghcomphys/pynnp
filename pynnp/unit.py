"""Unit"""

# ----------------------------------------------------------------------------
# Physical conversion constant
# ----------------------------------------------------------------------------
ANGSTROM_TO_BOHR = 1.8897261328
EV_TO_HARTREE = 0.0367493254
KCALMOL_TO_HARTREE = 0.001593602

HARTREE_TO_EV = 1./EV_TO_HARTREE
HARTREE_TO_MEV = HARTREE_TO_EV*1000.0

# ----------------------------------------------------------------------------
# Define utility constants, functions, and classes
# ----------------------------------------------------------------------------
class UnitConversion:
    """A class for unit conversion regarding file i/o."""

    def __init__(self, energy_conversion=1.0, length_conversion=1.0, charge_conversion=1.0):
        self.energy = energy_conversion
        self.length = length_conversion
        self.charge = charge_conversion
        self.force = energy_conversion / length_conversion

    def inverse(self):
        """A method that returns the inverse of UnitConversion object."""
        return UnitConversion(1.0 / self.energy, 1.0 / self.length, 1. / self.charge)

    @property
    def inverse(self):
        """A method that returns the inverse of UnitConversion object."""
        return self.inverse()
