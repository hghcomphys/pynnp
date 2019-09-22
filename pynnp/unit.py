"""Unit"""

# ----------------------------------------------------------------------------
# Physical conversion constant
# ----------------------------------------------------------------------------
ANGSTROM_TO_BOHR = 1.8897261328
EV_TO_HARTREE = 0.0367493254
KCALMOL_TO_HARTREE = 0.001593602

# ----------------------------------------------------------------------------
# Define utility constants, functions, and classes
# ----------------------------------------------------------------------------
class UnitConversion:
    """A class for unit conversion of RuNNer package."""

    def __init__(self, energy_conversion=1.0, length_conversion=1.0):
        self.energy = energy_conversion
        self.length = length_conversion
        self.charge = 1.0
        self.force = energy_conversion / length_conversion

    @property
    def inverse(self):
        """A method that applies inverse unit conversion."""
        return UnitConversion(1.0/self.energy, 1.0/self.length)
