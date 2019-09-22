"""data set"""

# ----------------------------------------------------------------------------
# Setup class for AtomicData
# ----------------------------------------------------------------------------
class AtomicData:
    """A class that holds atomic data such as positions, forces, total_energy, charges, etc."""

    def __init__(self, atomid=0, position=(0.0, 0.0, 0.0), symbol='X', charge=0.0, energy=0.0, force=(0.0, 0.0, 0.0)):
        self.atomid = atomid
        self.position= position
        self.symbol = symbol
        self.charge = charge
        self.energy = energy
        self.force = force

# ----------------------------------------------------------------------------
# Setup classes for CollectiveData
# ----------------------------------------------------------------------------
class CollectiveData:
    """A class that holds collective quantities of simulated system such as total energy or charge."""

    def __init__(self, cell=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), total_energy=0.0, total_charge=0.0):
            self.cell = cell
            self.total_energy = total_energy
            self.total_charge = total_charge

# ----------------------------------------------------------------------------
# Setup classes for Sample
# ----------------------------------------------------------------------------
class Sample:
    """ A class that holds a list of atomic data and also collective data for a single sample."""

    def __init__(self):
        self.atomic = []
        self.collective = None

    @property
    def number_of_atoms(self):
        return len(self.atomic)

    @property
    def total_energy(self):
        tot = 0.0
        for atom in self.atomic:
            tot += atom.energy
        return tot

    @property
    def total_charge(self):
        tot = 0.0
        for atom in self.atomic:
            tot += atom.charge
        return tot

    def get_atoms_for_symbol(self, symbol):
        sel_atoms = []
        for atom in self.atomic:
            if atom.symbol == symbol:
                sel_atoms.append(atom)
        return sel_atoms

    def get_number_of_atoms_for_symbol(self, symbol):
        return len(self.get_atoms_for_symbol(symbol))

# ----------------------------------------------------------------------------
# Setup classes for DataSet
# ----------------------------------------------------------------------------
class DataSet:
    """This class holds a collection of samples."""

    def __init__(self):
        self.samples = []

    def append(self, sample):
        """Append a sample to list of samples."""
        self.samples.append(sample)

    @property
    def number_of_samples(self):
        return len(self.samples)
